export interface PropertyItem {
  marketplace: string
  title: string
  price: number
  description: string
  location: string
  district: string
  area?: number
  rooms?: number
  url: string
  scraped_at: string
}

export interface CityInfo {
  name: string
  name_alt: string[]
  districts: string[]
  coordinates: number[]
}

export interface LocationSearchResult {
  cities: CityInfo[]
  total: number
}

