import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { contractAPI } from '../services/api';
import { useAuth } from './AuthContext';

const ContractContext = createContext();

export const useContract = () => {
  const context = useContext(ContractContext);
  if (!context) {
    throw new Error('useContract must be used within a ContractProvider');
  }
  return context;
};

export const ContractProvider = ({ children }) => {
  const [contracts, setContracts] = useState([]);
  const [expiringContracts, setExpiringContracts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  // Load all contracts
  const loadContracts = useCallback(async () => {
    if (!user?.email) return;

    setLoading(true);
    setError(null);
    try {
      console.log(`Loading contracts for user: ${user.email}`);
      const response = await contractAPI.getContracts(user.email);
      console.log('Contracts API response:', response.data);
      
      if (response.data.success) {
        setContracts(response.data.data || []);
        console.log(`Loaded ${response.data.data?.length || 0} contracts`);
      } else {
        setError('Unable to load contract list');
        console.error('API returned error:', response.data.message);
      }
    } catch (err) {
      setError('Server connection error');
      console.error('Error loading contracts:', err);
      console.error('Error details:', {
        message: err.message,
        status: err.response?.status,
        data: err.response?.data
      });
    } finally {
      setLoading(false);
    }
  }, [user?.email]);

  // Load expiring contracts (filtered from all contracts)
  const loadExpiringContracts = useCallback(async () => {
    if (!user?.email) return;

    setLoading(true);
    setError(null);
    try {
      // Get all contracts and filter for expiring ones
      const response = await contractAPI.getContracts(user.email);
      if (response.data.success) {
        const allContracts = response.data.data || [];
        
        // Filter contracts that are expiring soon (within 30 days)
        const now = new Date();
        const thirtyDaysFromNow = new Date(now.getTime() + (30 * 24 * 60 * 60 * 1000));
        
        const expiringContracts = allContracts.filter(contract => {
          if (!contract.contract_end_date) return false;
          
          const endDate = new Date(contract.contract_end_date);
          return endDate <= thirtyDaysFromNow && endDate >= now;
        });
        
        setExpiringContracts(expiringContracts);
        console.log(`Found ${expiringContracts.length} expiring contracts`);
      } else {
        setError('Unable to load contracts list');
      }
    } catch (err) {
      setError('Server connection error');
      console.error('Error loading expiring contracts:', err);
    } finally {
      setLoading(false);
    }
  }, [user?.email]);

  // Create new contract
  const createContract = async (contractData) => {
    if (!user?.email) return { success: false, message: 'Not logged in' };

    setLoading(true);
    setError(null);
    try {
      const response = await contractAPI.createContract({
        ...contractData,
        UserEmail: user.email
      });
      
      if (response.data.success) {
        await loadContracts(); // Reload contracts
        return { success: true, data: response.data.data };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (err) {
      const message = err.response?.data?.detail || 'Error creating contract';
      return { success: false, message };
    } finally {
      setLoading(false);
    }
  };

  // Update contract
  const updateContract = async (contractId, updateData) => {
    if (!user?.email) return { success: false, message: 'Not logged in' };

    setLoading(true);
    setError(null);
    try {
      const response = await contractAPI.updateContract(contractId, user.email, updateData);
      
      if (response.data.success) {
        await loadContracts(); // Reload contracts
        return { success: true, data: response.data.data };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (err) {
      const message = err.response?.data?.detail || 'Error updating contract';
      return { success: false, message };
    } finally {
      setLoading(false);
    }
  };

  // Delete contract
  const deleteContract = async (contractId) => {
    if (!user?.email) return { success: false, message: 'Not logged in' };

    setLoading(true);
    setError(null);
    try {
      const response = await contractAPI.deleteContract(contractId, user.email);
      
      if (response.data.success) {
        await loadContracts(); // Reload contracts
        return { success: true };
      } else {
        return { success: false, message: response.data.message };
      }
    } catch (err) {
      const message = err.response?.data?.detail || 'Error deleting contract';
      return { success: false, message };
    } finally {
      setLoading(false);
    }
  };

  // Load data when user changes
  useEffect(() => {
    if (user?.email) {
      loadContracts();
      // Load expiring contracts after contracts are loaded
      setTimeout(() => {
        loadExpiringContracts();
      }, 1000);
    }
  }, [user?.email, loadContracts, loadExpiringContracts]);

  const value = {
    contracts,
    expiringContracts,
    loading,
    error,
    loadContracts,
    loadExpiringContracts,
    createContract,
    updateContract,
    deleteContract,
  };

  return (
    <ContractContext.Provider value={value}>
      {children}
    </ContractContext.Provider>
  );
};
