<script lang="ts">
  import { query, mutation } from 'svelte-apollo';
  import { GET_USERS, CREATE_USER, UPDATE_USER, DELETE_USER } from '$lib/graphql/queries';
  import { Button, Card, Input, Alert } from '@synflict/ui';
  import { onMount } from 'svelte';
  
  // Query to fetch users from the GraphQL API
  const users = query(GET_USERS);
  
  // Mutations
  const createUserMutation = mutation(CREATE_USER);
  const updateUserMutation = mutation(UPDATE_USER);
  const deleteUserMutation = mutation(DELETE_USER);
  
  // Form state
  let showForm = false;
  let formMode: 'create' | 'edit' = 'create';
  let currentUserId = '';
  let formData = {
    name: '',
    email: '',
    role: 'user' as 'admin' | 'user'
  };
  let formError = '';
  
  // Reset form to default state
  function resetForm() {
    formMode = 'create';
    currentUserId = '';
    formData = {
      name: '',
      email: '',
      role: 'user'
    };
    formError = '';
  }
  
  // Open form for creating a new user
  function openCreateForm() {
    resetForm();
    showForm = true;
  }
  
  // Open form for editing an existing user
  function openEditForm(user: any) {
    formMode = 'edit';
    currentUserId = user.id;
    formData = {
      name: user.name,
      email: user.email,
      role: user.role
    };
    showForm = true;
  }
  
  // Handle form submission
  async function handleSubmit() {
    try {
      if (formMode === 'create') {
        await createUserMutation({ variables: { input: formData } });
      } else {
        await updateUserMutation({ 
          variables: { 
            id: currentUserId,
            input: formData 
          } 
        });
      }
      
      // Refetch users to update the list
      await users.refetch();
      
      // Close the form
      showForm = false;
      resetForm();
    } catch (error: any) {
      formError = error.message;
    }
  }
  
  // Handle user deletion
  async function handleDelete(id: string) {
    if (confirm('Are you sure you want to delete this user?')) {
      try {
        await deleteUserMutation({ variables: { id } });
        await users.refetch();
      } catch (error: any) {
        alert(`Error deleting user: ${error.message}`);
      }
    }
  }
  
  // Format date for display
  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString();
  }
</script>

<div class="container mx-auto px-4 py-8">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-bold text-gray-800">Users</h1>
    <Button type="primary" on:click={openCreateForm}>Add New User</Button>
  </div>
  
  {#if showForm}
    <Card padding="lg" shadow="md" rounded="md" border={true} class="mb-8">
      <h2 class="text-xl font-semibold mb-4">{formMode === 'create' ? 'Create New User' : 'Edit User'}</h2>
      
      {#if formError}
        <Alert type="error" dismissible={true} class="mb-4">{formError}</Alert>
      {/if}
      
      <form on:submit|preventDefault={handleSubmit} class="space-y-4">
        <Input 
          label="Name" 
          id="name" 
          bind:value={formData.name} 
          required 
        />
        
        <Input 
          type="email" 
          label="Email" 
          id="email" 
          bind:value={formData.email} 
          required 
        />
        
        <div class="w-full">
          <label for="role" class="block text-sm font-medium text-gray-700 mb-1">Role</label>
          <select 
            id="role" 
            bind:value={formData.role} 
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        
        <div class="flex justify-end space-x-3 pt-4">
          <Button type="ghost" on:click={() => { showForm = false; resetForm(); }}>Cancel</Button>
          <Button type="primary" on:click={handleSubmit}>{formMode === 'create' ? 'Create User' : 'Save Changes'}</Button>
        </div>
      </form>
    </Card>
  {/if}
  
  {#if $users.loading}
    <div class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
  {:else if $users.error}
    <Alert type="error" dismissible={true} class="mb-6">
      <p>Error loading users: {$users.error.message}</p>
      <div class="mt-3">
        <Button type="primary" size="sm" on:click={() => users.refetch()}>Try Again</Button>
      </div>
    </Alert>
  {:else}
    <div class="bg-white shadow overflow-hidden rounded-lg">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {#each $users.data.users as user (user.id)}
            <tr>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{user.name}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-500">{user.email}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {user.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-green-100 text-green-800'}">
                  {user.role}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {formatDate(user.createdAt)}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-2">
                  <Button type="secondary" size="sm" on:click={() => openEditForm(user)}>Edit</Button>
                  <Button type="danger" size="sm" on:click={() => handleDelete(user.id)}>Delete</Button>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>
