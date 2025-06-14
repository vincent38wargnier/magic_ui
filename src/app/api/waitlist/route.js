import { MongoClient } from 'mongodb';
import { NextResponse } from 'next/server';

const uri = process.env.MONGODB_URI || 'mongodb+srv://magify-test:9bKHW3DxnZTHvQMs@magify-test.sx207.mongodb.net/workflow';
const client = new MongoClient(uri);

export async function POST(request) {
  try {
    // Parse form data instead of JSON
    const formData = await request.formData();
    const name = formData.get('name');
    const email = formData.get('email');
    const industry = formData.get('industry');

    // Validate required fields
    if (!name || !email || !industry) {
      return NextResponse.json(
        { error: 'Name, email, and industry are required' },
        { status: 400 }
      );
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: 'Please enter a valid email address' },
        { status: 400 }
      );
    }

    // Connect to MongoDB
    await client.connect();
    const db = client.db('workflow');
    const collection = db.collection('mcpmyapi_waitlist');

    // Check if email already exists
    const existingEntry = await collection.findOne({ email });
    if (existingEntry) {
      return NextResponse.json(
        { error: 'This email is already on the waiting list' },
        { status: 409 }
      );
    }

    // Insert new entry
    const result = await collection.insertOne({
      name,
      email,
      industry,
      createdAt: new Date(),
      status: 'pending'
    });

    return NextResponse.json(
      { message: 'Successfully added to waiting list!', id: result.insertedId },
      { status: 201 }
    );

  } catch (error) {
    console.error('Error adding to waitlist:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  } finally {
    await client.close();
  }
} 