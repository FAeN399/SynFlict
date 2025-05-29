import { createSchema } from 'graphql-yoga';
import { db, User } from './database';

// Define the GraphQL schema
export const schema = createSchema({
  typeDefs: /* GraphQL */ `
    type Query {
      hello: String
      users: [User!]!
      user(id: ID!): User
    }

    type Mutation {
      createUser(input: CreateUserInput!): User!
      updateUser(id: ID!, input: UpdateUserInput!): User
      deleteUser(id: ID!): Boolean!
    }

    input CreateUserInput {
      name: String!
      email: String!
      role: UserRole!
    }

    input UpdateUserInput {
      name: String
      email: String
      role: UserRole
    }

    enum UserRole {
      admin
      user
    }

    type User {
      id: ID!
      name: String!
      email: String!
      role: UserRole!
      createdAt: String!
    }
  `,
  resolvers: {
    Query: {
      hello: () => 'Hello from GraphQL Yoga!',
      users: () => db.users.findAll(),
      user: (_, args: { id: string }) => db.users.findById(args.id)
    },
    Mutation: {
      createUser: (_, args: { input: Omit<User, 'id' | 'createdAt'> }) => {
        return db.users.create(args.input);
      },
      updateUser: (_, args: { id: string, input: Partial<Omit<User, 'id' | 'createdAt'>> }) => {
        return db.users.update(args.id, args.input);
      },
      deleteUser: (_, args: { id: string }) => {
        return db.users.delete(args.id);
      }
    },
    User: {
      // Convert Date to ISO string for GraphQL
      createdAt: (user: User) => user.createdAt.toISOString()
    }
  }
});
