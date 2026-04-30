import { describe, it, expect } from 'vitest'
import { formatCurrency, formatDate, formatTime, formatDateTime } from '../../../src/utils/format'

describe('formatCurrency', () => {
  it('금액을 원화 포맷으로 변환한다', () => {
    expect(formatCurrency(12500)).toBe('₩12,500')
  })

  it('0원을 올바르게 표시한다', () => {
    expect(formatCurrency(0)).toBe('₩0')
  })

  it('큰 금액을 올바르게 표시한다', () => {
    expect(formatCurrency(1000000)).toBe('₩1,000,000')
  })
})

describe('formatDate', () => {
  it('날짜를 yyyy.MM.dd 포맷으로 변환한다', () => {
    expect(formatDate('2026-04-30T14:30:00Z')).toMatch(/2026\.04\.30/)
  })
})

describe('formatTime', () => {
  it('시간을 HH:mm 포맷으로 변환한다', () => {
    const result = formatTime('2026-04-30T14:30:00Z')
    expect(result).toMatch(/\d{2}:\d{2}/)
  })
})

describe('formatDateTime', () => {
  it('날짜+시간을 yyyy.MM.dd HH:mm 포맷으로 변환한다', () => {
    const result = formatDateTime('2026-04-30T14:30:00Z')
    expect(result).toMatch(/2026\.04\.30 \d{2}:\d{2}/)
  })
})
