// src/components/AvatarUpload.tsx
'use client';

import { useState, useRef } from 'react';
import { useUser } from '@/contexts/UserContext';

export const AvatarUpload: React.FC = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { profile, uploadAvatar } = useUser();

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      setError('File size must be less than 5MB');
      return;
    }

    if (!file.type.startsWith('image/')) {
      setError('Please select an image file');
      return;
    }

    try {
      setIsUploading(true);
      setError(null);
      await uploadAvatar(file);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-4">
        <div className="w-16 h-16 bg-gray-300 rounded-full flex items-center justify-center">
          {profile?.avatar_url ? (
            <img
              src={profile.avatar_url}
              alt="Profile"
              className="w-16 h-16 rounded-full object-cover"
            />
          ) : (
            <span className="text-lg font-bold text-gray-600">
              {getUserInitials(profile)}
            </span>
          )}
        </div>

        <div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
            id="avatar-upload"
          />
          <label
            htmlFor="avatar-upload"
            className="cursor-pointer bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
          >
            {isUploading ? 'Uploading...' : 'Change Avatar'}
          </label>
        </div>
      </div>

      {error && (
        <p className="text-red-600 text-sm">{error}</p>
      )}

      <p className="text-sm text-gray-500">
        Supported formats: JPG, PNG, GIF. Max size: 5MB
      </p>
    </div>
  );
};