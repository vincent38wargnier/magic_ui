import { MongoClient, ObjectId } from 'mongodb';
import { NextResponse } from 'next/server';

const uri = process.env.MONGODB_URI || 'mongodb+srv://magify-test:9bKHW3DxnZTHvQMs@magify-test.sx207.mongodb.net/workflow';

// GET - Retrieve UI state
export async function GET(request) {
  let client;
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');

    if (!id) {
      return NextResponse.json(
        { error: 'UI ID parameter is required' },
        { status: 400 }
      );
    }

    if (!ObjectId.isValid(id)) {
      return NextResponse.json(
        { error: 'Invalid UI ID format' },
        { status: 400 }
      );
    }

    client = new MongoClient(uri);
    await client.connect();
    const db = client.db('workflow');
    const collection = db.collection('ui_components');

    const component = await collection.findOne({ _id: new ObjectId(id) });

    if (!component) {
      return NextResponse.json(
        { error: 'UI component not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      id: component._id,
      state: component.state || {},
      lastUpdated: component.stateUpdatedAt || component.createdAt
    }, { status: 200 });

  } catch (error) {
    console.error('Error retrieving UI state:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  } finally {
    if (client) {
      await client.close();
    }
  }
}

// POST - Update UI state
export async function POST(request) {
  let client;
  try {
    const { id, state } = await request.json();

    if (!id || !state) {
      return NextResponse.json(
        { error: 'UI ID and state are required' },
        { status: 400 }
      );
    }

    if (!ObjectId.isValid(id)) {
      return NextResponse.json(
        { error: 'Invalid UI ID format' },
        { status: 400 }
      );
    }

    client = new MongoClient(uri);
    await client.connect();
    const db = client.db('workflow');
    const collection = db.collection('ui_components');

    const result = await collection.updateOne(
      { _id: new ObjectId(id) },
      { 
        $set: { 
          state: state,
          stateUpdatedAt: new Date()
        }
      }
    );

    if (result.matchedCount === 0) {
      return NextResponse.json(
        { error: 'UI component not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      message: 'State updated successfully',
      id: id,
      state: state,
      lastUpdated: new Date()
    }, { status: 200 });

  } catch (error) {
    console.error('Error updating UI state:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  } finally {
    if (client) {
      await client.close();
    }
  }
} 