'use client'

import { PropertyItem } from '@/types'

interface StatsCardsProps {
  properties: PropertyItem[]
}

export default function StatsCards({ properties }: StatsCardsProps) {
  const stats = {
    total: properties.length,
    avgPrice: properties.length > 0
      ? Math.round(properties.reduce((sum, p) => sum + p.price, 0) / properties.length)
      : 0,
    minPrice: properties.length > 0
      ? Math.min(...properties.map(p => p.price))
      : 0,
    maxPrice: properties.length > 0
      ? Math.max(...properties.map(p => p.price))
      : 0,
    cities: new Set(properties.map(p => p.location)).size,
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-KZ', {
      style: 'currency',
      currency: 'KZT',
      minimumFractionDigits: 0,
    }).format(price)
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="text-sm text-gray-500 mb-1">Всего объявлений</div>
        <div className="text-2xl font-bold text-telegram-button">
          {stats.total}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="text-sm text-gray-500 mb-1">Средняя цена</div>
        <div className="text-2xl font-bold text-telegram-button">
          {formatPrice(stats.avgPrice)}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="text-sm text-gray-500 mb-1">Мин. цена</div>
        <div className="text-2xl font-bold text-green-600">
          {formatPrice(stats.minPrice)}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="text-sm text-gray-500 mb-1">Макс. цена</div>
        <div className="text-2xl font-bold text-red-600">
          {formatPrice(stats.maxPrice)}
        </div>
      </div>
    </div>
  )
}

