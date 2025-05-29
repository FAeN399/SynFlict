import fastify from 'fastify';
import { createYoga } from 'graphql-yoga';
import { schema } from './schema';

const app = fastify({ logger: true });

// Create Yoga instance
const yoga = createYoga({ schema });

// Register GraphQL Yoga as a Fastify route
app.route({
  url: '/graphql',
  method: ['GET', 'POST', 'OPTIONS'],
  handler: async (req, reply) => {
    // Handle preflight requests
    if (req.method === 'OPTIONS') {
      reply.header('Access-Control-Allow-Origin', '*');
      reply.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
      reply.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
      return reply.status(204).send();
    }

    // Handle the request with GraphQL Yoga
    const response = await yoga.handleNodeRequest(req, {
      req,
      reply
    });

    // Set response headers
    response.headers.forEach((value, key) => {
      reply.header(key, value);
    });

    reply.status(response.status);
    return reply.send(response.body);
  }
});

// Health check endpoint
app.get('/health', async () => {
  return { status: 'ok' };
});

// Start the server
const start = async () => {
  try {
    await app.listen({ port: 4000, host: '0.0.0.0' });
    console.log('Server is running on http://localhost:4000/graphql');
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

// Only start the server if this file is run directly
if (require.main === module) {
  start();
}

// Export for testing
export { app };
