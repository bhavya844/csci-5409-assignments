import bcryptjs from "bcryptjs";
import axios from "axios";


const createSalt = async (rounds) => {
  try {
    const salt = await bcryptjs.genSalt(rounds);
    return salt.replace("$2a$", "$2b$");
  } catch (err) {
    throw new Error("Error generating salt: " + err.message);
  }
};

export const handler = async (event) => {
  console.log("Received event:", JSON.stringify(event));

  
  const valueToHash = event.value;
  const operation = event.action; 

  if (!valueToHash) {
    console.error("No value to hash provided");
    return {
      statusCode: 400,
      body: JSON.stringify({ message: "No value to hash provided" }),
    };
  }

  
  const roundsOfSalt = 12;
  const salt = await createSalt(roundsOfSalt);
  const hashedValue = await bcryptjs.hash(valueToHash, salt);

  console.log("Original Value:", valueToHash);
  console.log("Hashed Value:", hashedValue);

  
  const postPayload = {
    banner: "B00982225", 
    result: hashedValue,
    arn: "arn:aws:lambda:us-east-1:970200206506:function:Bcrypt", 
    action: event.action || "bcrypt",
    value: valueToHash,
  };

  
  try {
    const response = await axios.post(event.course_uri, postPayload);
    console.log("POST request response:", response.data);

    return {
      statusCode: 200,
      body: JSON.stringify({
        message: `Hello from Lambda! Processed using ${operation}`,
        originalValue: valueToHash,
        hashedValue: hashedValue,
        postResponse: response.data,
      }),
    };
  } catch (error) {
    console.error("Error making POST request:", error);

    return {
      statusCode: 500,
      body: JSON.stringify({
        message: "Error making POST request",
        error: error.message,
      }),
    };
  }
};
