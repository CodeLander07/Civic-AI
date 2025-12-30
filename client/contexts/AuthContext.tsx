"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import api from '@/lib/axios';
import { supabase } from '@/lib/supabaseClient';
import { AxiosError } from 'axios';

interface User {
  id: string;
  email: string;
  name: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  signup: (name: string, email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user && !!token;

  const verifyUserToken = async (authToken: string) => {
    const response = await api.get('/auth/me', {
      headers: { Authorization: `Bearer ${authToken}` }
    });
    return response.data;
  };

  // Initialize auth state from localStorage
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const storedToken = localStorage.getItem('civic_ai_token');
        const storedUser = localStorage.getItem('civic_ai_user');

        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
          
          // Verify token is still valid
          const userData = await verifyUserToken(storedToken);
          setUser(userData);
          localStorage.setItem('civic_ai_user', JSON.stringify(userData));
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        // Clear invalid data
        localStorage.removeItem('civic_ai_token');
        localStorage.removeItem('civic_ai_user');
        setToken(null);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // Set up axios interceptor for auth token
  useEffect(() => {
    const requestInterceptor = api.interceptors.request.use(
      (config) => {
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    const responseInterceptor = api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token is invalid, logout user
          logout();
        }
        return Promise.reject(error);
      }
    );

    return () => {
      api.interceptors.request.eject(requestInterceptor);
      api.interceptors.response.eject(responseInterceptor);
    };
  }, [token]);

  const login = async (email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      setIsLoading(true);
      
      const response = await api.post('/auth/login', {
        email,
        password
      });

      const { access_token, user: userData } = response.data;

      // Store auth data
      setToken(access_token);
      setUser(userData);
      localStorage.setItem('civic_ai_token', access_token);
      localStorage.setItem('civic_ai_user', JSON.stringify(userData));

      return { success: true };
    } catch (error: unknown) {
      console.error('Login error:', error);
      
      let errorMessage = 'Login failed. Please try again.';
      
      if (error instanceof AxiosError) {
        if (error.response?.status === 401) {
          errorMessage = 'Invalid email or password.';
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.message) {
          errorMessage = error.message;
        }
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }

      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (name: string, email: string, password: string): Promise<{ success: boolean; error?: string }> => {
    try {
      setIsLoading(true);
      
      const response = await api.post('/auth/signup', {
        name,
        email,
        password
      });

      const { access_token, user: userData } = response.data;

      // Store auth data
      setToken(access_token);
      setUser(userData);
      localStorage.setItem('civic_ai_token', access_token);
      localStorage.setItem('civic_ai_user', JSON.stringify(userData));

      return { success: true };
    } catch (error: unknown) {
      console.error('Signup error:', error);
      
      let errorMessage = 'Account creation failed. Please try again.';
      
      if (error instanceof AxiosError) {
        if (error.response?.status === 400) {
          if (error.response.data?.detail?.includes('already registered')) {
            errorMessage = 'Email already registered. Please use a different email or try logging in.';
          } else if (error.response.data?.detail) {
            errorMessage = error.response.data.detail;
          }
        } else if (error.message) {
          errorMessage = error.message;
        }
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }

      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      await supabase.auth.signOut();
    } catch (error) {
      console.error('Error signing out:', error);
    }

    setUser(null);
    setToken(null);
    localStorage.removeItem('civic_ai_token');
    localStorage.removeItem('civic_ai_user');
    
    // Redirect to login page
    window.location.href = '/login';
  };

  const checkAuth = useCallback(async (): Promise<void> => {
    try {
      if (!token) {
        throw new Error('No token available');
      }

      const userData = await verifyUserToken(token);

      // Update user data
      setUser(userData);
      localStorage.setItem('civic_ai_user', JSON.stringify(userData));
    } catch (error) {
      console.error('Auth check failed:', error);
      // Clear invalid auth data
      setUser(null);
      setToken(null);
      localStorage.removeItem('civic_ai_token');
      localStorage.removeItem('civic_ai_user');
      throw error;
    }
  }, [token]);

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated,
    isLoading,
    login,
    signup,
    logout,
    checkAuth
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};