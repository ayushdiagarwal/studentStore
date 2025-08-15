import React, { useMemo, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

// Editable hostel lists
const BOYS_HOSTELS = [
  'Hostel A',
  'Hostel B',
  'Hostel C',
  'Hostel D',
  'Hostel J',
  'Hostel H',
  'Hostel K',
];

const GIRLS_HOSTELS = [
  'Hostel Q',
  'Hostel L',
  'Hostel I',
  'Hostel E',
  'Hostel PG',
  'Hostel FRF',
  'Hostel FRG',
];

const UserProfile: React.FC = () => {
  const { state, logout, updateUser } = useAuth();
  const [open, setOpen] = useState(false);

  const availableHostels = useMemo(() => {
    if (state.user?.gender === 'male') return BOYS_HOSTELS;
    if (state.user?.gender === 'female') return GIRLS_HOSTELS;
    return [];
  }, [state.user?.gender]);

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  if (!state.user) {
    return null;
  }

  return (
    <div className="relative flex items-center space-x-4">
      <div
        className="flex items-center space-x-3 cursor-pointer"
        onClick={() => setOpen((v) => !v)}
      >
        {state.user.profile_picture ? (
          <img
            src={state.user.profile_picture}
            alt={state.user.name}
            className="w-10 h-10 rounded-full border-2 border-gray-200"
          />
        ) : (
          <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
            <span className="text-gray-600 font-medium text-sm">
              {state.user.name.charAt(0).toUpperCase()}
            </span>
          </div>
        )}
        <div className="hidden md:block">
          <p className="text-sm font-medium text-gray-900">{state.user.name}</p>
          <p className="text-xs text-gray-500">{state.user.email}</p>
        </div>
      </div>

      {open && (
        <div className="absolute right-0 top-12 w-80 bg-white border rounded-lg shadow-lg p-4 z-50">
          <div className="flex items-center space-x-3 mb-3">
            {state.user.profile_picture ? (
              <img
                src={state.user.profile_picture}
                alt={state.user.name}
                className="w-12 h-12 rounded-full border"
              />
            ) : (
              <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center">
                <span className="text-gray-600 font-medium">
                  {state.user.name.charAt(0).toUpperCase()}
                </span>
              </div>
            )}
            <div>
              <p className="text-sm font-semibold text-gray-900">{state.user.name}</p>
              <p className="text-xs text-gray-500">{state.user.email}</p>
            </div>
          </div>

          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Gender</label>
              <div className="flex items-center space-x-4">
                <label className="inline-flex items-center space-x-2 text-sm">
                  <input
                    type="radio"
                    name="gender"
                    value="male"
                    checked={state.user.gender === 'male'}
                    onChange={() => updateUser({ gender: 'male', hostel: undefined })}
                    className="text-blue-600 focus:ring-blue-500"
                  />
                  <span>Male</span>
                </label>
                <label className="inline-flex items-center space-x-2 text-sm">
                  <input
                    type="radio"
                    name="gender"
                    value="female"
                    checked={state.user.gender === 'female'}
                    onChange={() => updateUser({ gender: 'female', hostel: undefined })}
                    className="text-blue-600 focus:ring-blue-500"
                  />
                  <span>Female</span>
                </label>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">Hostel</label>
              <select
                className="w-full border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={state.user.hostel || ''}
                onChange={(e) => updateUser({ hostel: e.target.value })}
                disabled={!state.user.gender}
              >
                <option value="" disabled>
                  {state.user.gender ? 'Select hostel' : 'Select gender first'}
                </option>
                {availableHostels.map((h) => (
                  <option key={h} value={h}>
                    {h}
                  </option>
                ))}
              </select>
              {!state.user.gender && (
                <p className="mt-1 text-xs text-gray-500">Choose gender to see hostels.</p>
              )}
            </div>

            <button
              onClick={handleLogout}
              disabled={state.isLoading}
              className="w-full inline-flex items-center justify-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
            >
              {state.isLoading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Logging out...
                </>
              ) : (
                'Logout'
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
