const express = require("express");
const application = express();
application.use(express.json());
const mysql2 = require("mysql2");

const databaseConnection = mysql2.createConnection({
  host: "assigment2-rds.czho2iyju1ye.us-east-1.rds.amazonaws.com",
  user: "admin",
  password: "bhavya123",
  database: "assignment2",
});

databaseConnection.connect((error) => {
  if (error) {
    throw error;
  }
  console.log("MySQL Connected...");
});

application.get("/list-products", (request, response) => {
  let selectQuery = "SELECT * FROM products";
  databaseConnection.query(selectQuery, (error, rows) => {
    if (error) {
      console.log(error);
      response.status(500).send("Error querying the database");
      return;
    }

    const productArray = rows.map((row) => ({
      name: row.name,
      price: row.price,
      availability: row.availability === 1,
    }));

    response.status(200).send({ products: productArray });
  });
});

application.post("/store-products", (request, response) => {
  let productArray = request.body.products;

  if (!Array.isArray(productArray) || request.body.products.length == 0) {
    const error = { error: "Invalid JSON input." };
    return response.status(400).send(error);
  }

  let insertQuery = "INSERT INTO products (name, price, availability) VALUES ?";
  let insertValues = productArray.map((product) => [
    product.name,
    product.price,
    product.availability,
  ]);

  databaseConnection.query(insertQuery, [insertValues], (error, result) => {
    if (error) {
      console.log(error);
    }
    response.status(200).send({ message: "Success." });
  });
});



const SERVER_PORT = 5000;

application.listen(SERVER_PORT, () =>
  console.log(`Server started on port ${SERVER_PORT}`)
);
