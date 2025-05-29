// Simple in-memory database for demonstration purposes
// In a real application, this would be replaced with a proper database like PostgreSQL, MongoDB, etc.

export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: Date;
}

// Initial seed data
const users: User[] = [
  {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    role: 'admin',
    createdAt: new Date('2025-01-15')
  },
  {
    id: '2',
    name: 'Jane Smith',
    email: 'jane@example.com',
    role: 'user',
    createdAt: new Date('2025-02-20')
  },
  {
    id: '3',
    name: 'Bob Johnson',
    email: 'bob@example.com',
    role: 'user',
    createdAt: new Date('2025-03-10')
  }
];

// Database operations
export const db = {
  users: {
    findAll: () => [...users],
    findById: (id: string) => users.find(user => user.id === id),
    create: (userData: Omit<User, 'id' | 'createdAt'>) => {
      const newUser: User = {
        ...userData,
        id: String(users.length + 1),
        createdAt: new Date()
      };
      users.push(newUser);
      return newUser;
    },
    update: (id: string, userData: Partial<Omit<User, 'id' | 'createdAt'>>) => {
      const index = users.findIndex(user => user.id === id);
      if (index === -1) return null;
      
      users[index] = {
        ...users[index],
        ...userData
      };
      
      return users[index];
    },
    delete: (id: string) => {
      const index = users.findIndex(user => user.id === id);
      if (index === -1) return false;
      
      users.splice(index, 1);
      return true;
    }
  }
};
