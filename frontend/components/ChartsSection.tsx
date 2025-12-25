'use client'

import { PropertyItem } from '@/types'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from 'recharts'

interface ChartsSectionProps {
  properties: PropertyItem[]
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d']

export default function ChartsSection({ properties }: ChartsSectionProps) {
  // График по городам
  const cityData = properties.reduce((acc, prop) => {
    const city = prop.location || 'Не указано'
    acc[city] = (acc[city] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  const cityChartData = Object.entries(cityData)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 10)

  // График распределения цен
  const priceRanges = [
    { range: '0-100k', min: 0, max: 100000 },
    { range: '100k-300k', min: 100000, max: 300000 },
    { range: '300k-500k', min: 300000, max: 500000 },
    { range: '500k-1M', min: 500000, max: 1000000 },
    { range: '1M+', min: 1000000, max: Infinity },
  ]

  const priceData = priceRanges.map(range => ({
    range: range.range,
    count: properties.filter(p => p.price >= range.min && p.price < range.max).length,
  }))

  // График по районам
  const districtData = properties
    .filter(p => p.district && p.district !== 'Не указано')
    .reduce((acc, prop) => {
      const district = prop.district
      acc[district] = (acc[district] || 0) + 1
      return acc
    }, {} as Record<string, number>)

  const districtChartData = Object.entries(districtData)
    .map(([name, value]) => ({ name, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 8)

  // График средних цен по городам
  const avgPriceByCity = properties.reduce((acc, prop) => {
    const city = prop.location || 'Не указано'
    if (!acc[city]) {
      acc[city] = { total: 0, count: 0 }
    }
    acc[city].total += prop.price
    acc[city].count += 1
    return acc
  }, {} as Record<string, { total: number; count: number }>)

  const avgPriceData = Object.entries(avgPriceByCity)
    .map(([name, data]) => ({
      name,
      avgPrice: Math.round(data.total / data.count),
    }))
    .sort((a, b) => b.avgPrice - a.avgPrice)
    .slice(0, 10)

  return (
    <div className="space-y-6 mb-6">
      <h2 className="text-xl font-bold">Графики и статистика</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* График по городам */}
        <div className="bg-white rounded-lg shadow-md p-4">
          <h3 className="text-lg font-semibold mb-4">Объявления по городам</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={cityChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#0088FE" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Распределение цен */}
        <div className="bg-white rounded-lg shadow-md p-4">
          <h3 className="text-lg font-semibold mb-4">Распределение цен</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={priceData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ range, percent }) => `${range}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="count"
              >
                {priceData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Средние цены по городам */}
        <div className="bg-white rounded-lg shadow-md p-4">
          <h3 className="text-lg font-semibold mb-4">Средние цены по городам</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={avgPriceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip formatter={(value) => `${value.toLocaleString('ru-KZ')} ₸`} />
              <Line type="monotone" dataKey="avgPrice" stroke="#8884d8" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* График по районам */}
        {districtChartData.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-4">
            <h3 className="text-lg font-semibold mb-4">Объявления по районам</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={districtChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#00C49F" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  )
}

