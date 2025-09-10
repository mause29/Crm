import React, { useState, useEffect } from 'react';

function Profile({ user }) {
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!user) return;

    const fetchProfile = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch('http://127.0.0.1:8000/users/me', {
          headers: {
            Authorization: `Bearer ${user.access_token}`,
          },
        });
        if (!response.ok) {
          throw new Error('Failed to fetch profile data');
        }
        const data = await response.json();
        setProfileData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [user]);

  if (loading) {
    return <div className="p-4 text-center text-gray-600">Cargando perfil de usuario...</div>;
  }

  if (error) {
    return (
      <div className="p-4 text-center text-red-600">
        <p>Error al cargar el perfil: {error}</p>
      </div>
    );
  }

  if (!profileData) {
    return <div className="p-4 text-center text-gray-600">No hay datos de perfil disponibles.</div>;
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow-md mt-6 max-w-md mx-auto">
      <h2 className="text-xl font-semibold mb-4">Perfil de Usuario</h2>
      <p><strong>Nombre:</strong> {profileData.name || 'N/A'}</p>
      <p><strong>Email:</strong> {profileData.email || 'N/A'}</p>
      <p><strong>Rol:</strong> {profileData.role || 'N/A'}</p>
      <p><strong>Fecha de Registro:</strong> {new Date(profileData.created_at).toLocaleDateString('es-ES')}</p>
      {/* Add more profile fields as needed */}
    </div>
  );
}

export default Profile;
