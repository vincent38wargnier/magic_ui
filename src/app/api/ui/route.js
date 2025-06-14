import { MongoClient, ObjectId } from 'mongodb';
import { NextResponse } from 'next/server';

const uri = process.env.MONGODB_URI || 'mongodb+srv://magify-test:9bKHW3DxnZTHvQMs@magify-test.sx207.mongodb.net/workflow';
const client = new MongoClient(uri);

export async function POST(request) {
  try {
    const body = await request.json();
    const { html, js, content } = body;

    // Support both single content field and separate html/js fields
    let finalHtml = '';
    let finalJs = '';

    if (content) {
      // Use content as complete HTML (may include inline JS)
      finalHtml = content;
      finalJs = '';
    } else if (html || js) {
      // Use separate html and js fields
      finalHtml = html || '';
      finalJs = js || '';
    } else {
      return NextResponse.json(
        { error: 'Either "content" field or "html"/"js" fields are required' },
        { status: 400 }
      );
    }

    // Connect to MongoDB
    await client.connect();
    const db = client.db('workflow');
    const collection = db.collection('ui_components');

    // Insert new UI component
    const result = await collection.insertOne({
      html: finalHtml,
      js: finalJs,
      content: content || null,
      createdAt: new Date(),
      status: 'active'
    });

    const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000';
    const displayUrl = `${baseUrl}/ui/${result.insertedId}`;

    return NextResponse.json(
      { 
        message: 'UI component stored successfully!', 
        id: result.insertedId,
        url: displayUrl
      },
      { status: 201 }
    );

  } catch (error) {
    console.error('Error storing UI component:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  } finally {
    await client.close();
  }
}

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');

    if (!id) {
      return NextResponse.json(
        { error: 'ID parameter is required' },
        { status: 400 }
      );
    }

    // Validate ObjectId format
    if (!ObjectId.isValid(id)) {
      return NextResponse.json(
        { error: 'Invalid ID format' },
        { status: 400 }
      );
    }

    // Connect to MongoDB
    await client.connect();
    const db = client.db('workflow');
    const collection = db.collection('ui_components');

    // Find the UI component
    const component = await collection.findOne({ _id: new ObjectId(id) });

    if (!component) {
      return NextResponse.json(
        { error: 'UI component not found' },
        { status: 404 }
      );
    }

    return NextResponse.json(component, { status: 200 });

  } catch (error) {
    console.error('Error retrieving UI component:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  } finally {
    await client.close();
  }
} 