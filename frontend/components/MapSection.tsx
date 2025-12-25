'use client'

import { useEffect, useState } from 'react'
import { PropertyItem } from '@/types'
import axios from 'axios'

interface MapSectionProps {
  properties: PropertyItem[]
}

export default function MapSection({ properties }: MapSectionProps) {
  const [mapUrl, setMapUrl] = useState<string>('')
  const [loading, setLoading] = useState(false)

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    if (properties.length > 0) {
      generateMap()
    }
  }, [properties])

  const generateMap = async () => {
    setLoading(true)
    try {
      // Для демонстрации используем примерные координаты
      // В реальном приложении нужно геокодировать адреса
      const markers = properties.slice(0, 50).map((prop, index) => {
        // Примерные координаты для Алматы (можно улучшить с помощью геокодинга)
        const baseLat = 43.2220
        const baseLon = 76.8512
        // Небольшое случайное смещение для визуализации
        const offset = 0.01
        return {
          lat: baseLat + (Math.random() - 0.5) * offset * 2,
          lon: baseLon + (Math.random() - 0.5) * offset * 2,
          title: prop.title.substring(0, 50),
          price: prop.price,
          url: prop.url,
        }
      })

      const response = await axios.post(`${apiUrl}/api/maps/generate`, {
        markers,
        center_lat: 43.2220,
        center_lon: 76.8512,
        zoom: 12,
      })

      if (response.data.success) {
        setMapUrl(`${apiUrl}${response.data.map_url}`)
      }
    } catch (error) {
      console.error('Error generating map:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <h3 className="text-lg font-semibold mb-4">Карта объявлений</h3>
        <div className="h-96 flex items-center justify-center">
          <p className="text-gray-500">Генерация карты...</p>
        </div>
      </div>
    )
  }

  if (!mapUrl) {
    return null
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-6">
      <h3 className="text-lg font-semibold mb-4">Карта объявлений</h3>
      <div className="h-96 rounded-lg overflow-hidden border">
        <iframe
          src={mapUrl}
          className="w-full h-full"
          style={{ border: 'none' }}
          title="Карта объявлений"
        />
      </div>
      <p className="text-sm text-gray-500 mt-2">
        Показано {Math.min(properties.length, 50)} объявлений на карте
      </p>
    </div>
  )
}

