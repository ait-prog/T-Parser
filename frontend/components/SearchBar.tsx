'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { LocationSearchResult } from '@/types'

interface SearchBarProps {
  onSearch: (url: string) => void
  onLocationSelect: (city: string, district?: string) => void
  loading: boolean
}

export default function SearchBar({ onSearch, onLocationSelect, loading }: SearchBarProps) {
  const [url, setUrl] = useState('')
  const [showLocationSearch, setShowLocationSearch] = useState(false)
  const [locationQuery, setLocationQuery] = useState('')
  const [locationResults, setLocationResults] = useState<LocationSearchResult | null>(null)
  const [selectedCity, setSelectedCity] = useState<string>('')
  const [selectedDistrict, setSelectedDistrict] = useState<string>('')
  const [districts, setDistricts] = useState<string[]>([])

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    if (locationQuery.length >= 2) {
      const timer = setTimeout(() => {
        searchLocations(locationQuery)
      }, 300)
      return () => clearTimeout(timer)
    } else {
      setLocationResults(null)
    }
  }, [locationQuery])

  const searchLocations = async (query: string) => {
    try {
      const response = await axios.get(`${apiUrl}/api/locations/search`, {
        params: { query }
      })
      setLocationResults({
        cities: response.data.cities || [],
        total: (response.data.cities?.length || 0) + (response.data.districts?.length || 0)
      })
    } catch (error) {
      console.error('Error searching locations:', error)
    }
  }

  const handleCitySelect = async (cityName: string) => {
    setSelectedCity(cityName)
    setLocationQuery(cityName)
    setShowLocationSearch(false)
    
    try {
      const response = await axios.get(`${apiUrl}/api/locations/districts`, {
        params: { city: cityName }
      })
      setDistricts(response.data.districts || [])
      onLocationSelect(cityName)
    } catch (error) {
      console.error('Error fetching districts:', error)
    }
  }

  const handleDistrictSelect = (district: string) => {
    setSelectedDistrict(district)
    onLocationSelect(selectedCity, district)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (url.trim()) {
      onSearch(url.trim())
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            URL страницы krisha.kz
          </label>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://krisha.kz/arenda/kvartiry/almaty/..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-telegram-button focus:border-transparent"
            disabled={loading}
          />
        </div>

        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => setShowLocationSearch(!showLocationSearch)}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
          >
            {showLocationSearch ? 'Скрыть' : 'Поиск по адресу'}
          </button>
          <button
            type="submit"
            disabled={loading || !url.trim()}
            className="flex-1 px-4 py-2 bg-telegram-button text-telegram-button-text rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {loading ? 'Парсинг...' : 'Спарсить'}
          </button>
        </div>
      </form>

      {showLocationSearch && (
        <div className="mt-4 pt-4 border-t">
          <label className="block text-sm font-medium mb-2">
            Поиск города или района
          </label>
          <input
            type="text"
            value={locationQuery}
            onChange={(e) => setLocationQuery(e.target.value)}
            placeholder="Начните вводить название города..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-telegram-button focus:border-transparent mb-2"
          />

          {locationQuery && locationResults && (
            <div className="mt-2 space-y-2">
              {locationResults.cities.map((city) => (
                <button
                  key={city.name}
                  onClick={() => handleCitySelect(city.name)}
                  className="block w-full text-left px-3 py-2 bg-gray-50 hover:bg-gray-100 rounded-lg transition"
                >
                  <div className="font-medium">{city.name}</div>
                  <div className="text-xs text-gray-500">
                    {city.districts.length} районов
                  </div>
                </button>
              ))}
            </div>
          )}

          {selectedCity && districts.length > 0 && (
            <div className="mt-4">
              <label className="block text-sm font-medium mb-2">
                Выберите район ({selectedCity})
              </label>
              <select
                value={selectedDistrict}
                onChange={(e) => handleDistrictSelect(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value="">Все районы</option>
                {districts.map((district) => (
                  <option key={district} value={district}>
                    {district}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

