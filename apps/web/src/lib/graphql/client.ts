import { ApolloClient, InMemoryCache, HttpLink, NormalizedCacheObject } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

// Create an HTTP link to the GraphQL API
const httpLink = new HttpLink({
  uri: 'http://localhost:4000/graphql',
});

// Create an auth link to add authentication headers if needed
const authLink = setContext((_: any, { headers }: { headers?: Record<string, string> }) => {
  // Get the authentication token from local storage if it exists
  const token = typeof localStorage !== 'undefined' ? localStorage.getItem('authToken') : null;
  
  // Return the headers to the context so httpLink can read them
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : '',
    }
  };
});

// Create the Apollo client
export const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
    },
  },
});
