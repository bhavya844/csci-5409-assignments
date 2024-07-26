import bcryptjs from "bcryptjs";
import axios from "axios";

// Helper function to generate a salt
const generateSalt = async (saltRounds) => {
  try {
    const salt = await bcryptjs.genSalt(saltRounds);
    return salt.replace("$2a$", "$2b$");
  } catch (err) {
    throw new Error("Error generating salt: " + err.message);
  }
};

export const handler = async (event) => {
  console.log("Received event:", JSON.stringify(event));

  // Directly access inputData from the event object
  const dataToHash = event.value;
  const action = event.action; // Directly access inputType

  if (!dataToHash) {
    console.error("No data to hash provided");
    return {
      statusCode: 400,
      body: JSON.stringify({ message: "No data to hash provided" }),
    };
  }

  // Perform hashing using bcryptjs
  const saltRounds = 12;
  const salt = await generateSalt(saltRounds);
  const hashedData = await bcryptjs.hash(dataToHash, salt);

  console.log("Original Data:", dataToHash);
  console.log("Hashed Data:", hashedData);

  // Prepare the data to send in the POST request
  const postData = {
    banner: "B00982225", // Assuming 'banner' is part of the event
    result: hashedData,
    arn: "arn:aws:lambda:us-east-1:970200206506:function:Bcrypt", // Assuming 'arn' is part of the event
    action: event.action || "bcrypt",
    value: dataToHash,
  };

  // Send the POST request to the course_uri
  try {
    const response = await axios.post(event.course_uri, postData);
    console.log("POST request response:", response.data);

    return {
      statusCode: 200,
      body: JSON.stringify({
        message: `Hello from Lambda! Processed using ${action}`,
        originalData: dataToHash,
        hashedData: hashedData,
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
