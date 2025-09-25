// api/contact.js
import { MongoClient } from "mongodb";

const MONGO_URL = process.env.MONGO_URL;
const DB_NAME = process.env.DB_NAME || "softgemz_database";
const CORS_ORIGINS = process.env.CORS_ORIGINS || "*";

let mongoClientPromise;
if (!global._mongoClientPromise) {
  const client = new MongoClient(MONGO_URL);
  global._mongoClientPromise = client.connect();
}
mongoClientPromise = global._mongoClientPromise;

export default async function handler(req, res) {
  // Basic CORS support (safe if frontend is hosted on same domain)
  res.setHeader("Access-Control-Allow-Origin", CORS_ORIGINS);
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ success: false, message: "Method not allowed" });
  }

  try {
    const { name, email, message } = req.body || {};
    if (!name || !email || !message) {
      return res.status(400).json({ success: false, message: "All fields required" });
    }

    const client = await mongoClientPromise;
    const db = client.db(DB_NAME);
    const collection = db.collection("contacts");

    const result = await collection.insertOne({
      name,
      email,
      message,
      createdAt: new Date()
    });

    return res.status(201).json({ success: true, message: "Saved", id: result.insertedId });
  } catch (err) {
    console.error("DB error:", err);
    return res.status(500).json({ success: false, message: "Database error" });
  }
}
