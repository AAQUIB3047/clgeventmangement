import { useState, useCallback } from 'react';

/**
 * useApi Hook - Example
 * Handles API calls with loading, error, and data states
 *
 * @param {string} url - API endpoint
 * @param {object} options - fetch options
 * @returns {object} {data, loading, error, refetch}
 */
export const useApi = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  }, [url, options]);

  return { data, loading, error, refetch: fetchData };
};

/**
 * useForm Hook - Example
 * Manages form state and validation
 *
 * @param {object} initialValues - initial form values
 * @param {function} onSubmit - submit handler
 * @returns {object} {values, errors, handleChange, handleSubmit, isSubmitting}
 */
export const useForm = (initialValues, onSubmit) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = useCallback(
    (e) => {
      const { name, value, type, checked } = e.target;
      setValues((prev) => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value,
      }));
      // Clear error when user starts typing
      if (errors[name]) {
        setErrors((prev) => ({
          ...prev,
          [name]: '',
        }));
      }
    },
    [errors]
  );

  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      setIsSubmitting(true);
      try {
        await onSubmit(values);
      } catch (err) {
        setErrors((prev) => ({
          ...prev,
          submit: err.message,
        }));
      } finally {
        setIsSubmitting(false);
      }
    },
    [values, onSubmit]
  );

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
  }, [initialValues]);

  return {
    values,
    errors,
    handleChange,
    handleSubmit,
    isSubmitting,
    reset,
    setValues,
  };
};

/**
 * useLocalStorage Hook - Example
 * Syncs state with localStorage
 *
 * @param {string} key - localStorage key
 * @param {any} initialValue - initial value
 * @returns {array} [storedValue, setValue]
 */
export const useLocalStorage = (key, initialValue) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value) => {
      try {
        const valueToStore = value instanceof Function ? value(storedValue) : value;
        setStoredValue(valueToStore);
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
      } catch (error) {
        console.error('Error writing to localStorage:', error);
      }
    },
    [key, storedValue]
  );

  return [storedValue, setValue];
};

/**
 * usePagination Hook - Example
 * Handles pagination logic
 *
 * @param {array} items - items to paginate
 * @param {number} itemsPerPage - items per page
 * @returns {object} {currentPage, totalPages, currentItems, goToPage, nextPage, prevPage}
 */
export const usePagination = (items, itemsPerPage = 10) => {
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(items.length / itemsPerPage);

  const currentItems = items.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

  const goToPage = useCallback(
    (page) => {
      const pageNumber = Math.max(1, Math.min(page, totalPages));
      setCurrentPage(pageNumber);
    },
    [totalPages]
  );

  const nextPage = useCallback(() => {
    goToPage(currentPage + 1);
  }, [currentPage, goToPage]);

  const prevPage = useCallback(() => {
    goToPage(currentPage - 1);
  }, [currentPage, goToPage]);

  return {
    currentPage,
    totalPages,
    currentItems,
    goToPage,
    nextPage,
    prevPage,
  };
};

/**
 * useDebounce Hook - Example
 * Debounces value changes
 *
 * @param {any} value - value to debounce
 * @param {number} delay - debounce delay in ms
 * @returns {any} debounced value
 */
export const useDebounce = (value, delay = 500) => {
  const [debouncedValue, setDebouncedValue] = useState(value);

  React.useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
};

export default {
  useApi,
  useForm,
  useLocalStorage,
  usePagination,
  useDebounce,
};
