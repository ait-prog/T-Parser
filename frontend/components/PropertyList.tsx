'use client'

import { PropertyItem } from '@/types'

interface PropertyListProps {
  properties: PropertyItem[]
}

export default function PropertyList({ properties }: PropertyListProps) {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-KZ', {
      style: 'currency',
      currency: 'KZT',
      minimumFractionDigits: 0,
    }).format(price)
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold mb-4">Список объявлений</h2>
      <div className="space-y-3">
        {properties.map((property, index) => (
          <div
            key={index}
            className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition"
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold flex-1">{property.title}</h3>
              <span className="text-xl font-bold text-telegram-button ml-4">
                {formatPrice(property.price)}
              </span>
            </div>

            <p className="text-gray-600 text-sm mb-3 line-clamp-2">
              {property.description}
            </p>

            <div className="flex flex-wrap gap-4 text-sm text-gray-500">
              <span>📍 {property.location}</span>
              {property.district && property.district !== 'Не указано' && (
                <span>🏘️ {property.district}</span>
              )}
              {property.area && <span>📐 {property.area} м²</span>}
              {property.rooms && <span>🚪 {property.rooms} комн.</span>}
            </div>

            <div className="mt-3 flex justify-between items-center">
              <span className="text-xs text-gray-400">
                {property.scraped_at}
              </span>
              <a
                href={property.url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-1 bg-telegram-button text-telegram-button-text rounded text-sm hover:opacity-90 transition"
              >
                Открыть
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

