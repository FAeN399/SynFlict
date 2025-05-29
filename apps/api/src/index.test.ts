import { describe, it, expect } from 'vitest';
import { app } from './index';

describe('API Server', () => {
  it('health endpoint returns ok status', async () => {
    const response = await app.inject({
      method: 'GET',
      url: '/health'
    });

    expect(response.statusCode).toBe(200);
    expect(JSON.parse(response.body)).toEqual({ status: 'ok' });
  });

  it('graphql endpoint is available', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/graphql',
      payload: {
        query: '{ hello }'
      }
    });

    expect(response.statusCode).toBe(200);
    const body = JSON.parse(response.body);
    expect(body.data.hello).toBe('Hello from GraphQL Yoga!');
  });
});
