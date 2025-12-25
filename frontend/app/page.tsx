'use client'

import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import { initData } from '@twa-dev/sdk'
import SearchBar from '@/components/SearchBar'
import PropertyList from '@/components/PropertyList'
import StatsCards from '@/components/StatsCards'
import ChartsSection from '@/components/ChartsSection'
import MapSection from '@/components/MapSection'
import { PropertyItem } from '@/types'

// Динамический импорт для избежания SSR проблем с Leaflet
const MapSectionDynamic = dynamic(() => import('@/components/MapSection'), {
  ssr: false
})

export default function Home() {
  const [properties, setProperties] = useState<PropertyItem[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedCity, setSelectedCity] = useState<string>('')
  const [selectedDistrict, setSelectedDistrict] = useState<string>('')

  useEffect(() => {
    // Инициализация Telegram Mini App
    if (typeof window !== 'undefined' && (window as any).Telegram?.WebApp) {
      try {
        const tg = (window as any).Telegram.WebApp
        tg.ready()
        tg.expand()
        
        // Применяем тему Telegram
        if (tg.themeParams) {
          const root = document.documentElement
          if (tg.themeParams.bg_color) {
            root.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color)
          }
          if (tg.themeParams.text_color) {
            root.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color)
          }
          if (tg.themeParams.hint_color) {
            root.style.setProperty('--tg-theme-hint-color', tg.themeParams.hint_color)
          }
          if (tg.themeParams.button_color) {
            root.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color)
          }
          if (tg.themeParams.button_text_color) {
            root.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color)
          }
        }
        
        console.log('Telegram Mini App initialized')
      } catch (error) {
        console.error('Error initializing Telegram Mini App:', error)
      }
    }
  }, [])

  const handleSearch = async (url: string) => {
    setLoading(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/parser/scrape?url=${encodeURIComponent(url)}`)
      const data = await response.json()
      
      if (data.success) {
        setProperties(data.items)
      } else {
        alert('Ошибка при парсинге: ' + (data.message || 'Неизвестная ошибка'))
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Ошибка при подключении к серверу')
    } finally {
      setLoading(false)
    }
  }

  const handleLocationSelect = (city: string, district?: string) => {
    setSelectedCity(city)
    setSelectedDistrict(district || '')
  }

  return (
    <main className="min-h-screen bg-telegram-bg text-telegram-text">
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        <header className="mb-6">
          <h1 className="text-2xl font-bold mb-2">Krisha.kz Parser</h1>
          <p className="text-telegram-hint text-sm">
            Парсер объявлений с графиками и картами
          </p>
        </header>

        <SearchBar 
          onSearch={handleSearch} 
          onLocationSelect={handleLocationSelect}
          loading={loading}
        />

        {properties.length > 0 && (
          <>
            <StatsCards properties={properties} />
            <ChartsSection properties={properties} />
            <MapSectionDynamic properties={properties} />
            <PropertyList properties={properties} />
          </>
        )}

        {properties.length === 0 && !loading && (
          <div className="text-center py-12 text-telegram-hint">
            <p>Введите URL страницы krisha.kz для начала парсинга</p>
          </div>
        )}
      </div>
    </main>
  )
}

