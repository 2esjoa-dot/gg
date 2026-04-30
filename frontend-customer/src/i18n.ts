import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import ko from './locales/ko/translation.json'

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      ko: { translation: ko },
    },
    fallbackLng: 'ko',
    supportedLngs: ['ko', 'en', 'zh', 'ja', 'es'],
    interpolation: { escapeValue: false },
  })

const loadLanguage = async (lng: string) => {
  if (i18n.hasResourceBundle(lng, 'translation')) return
  try {
    const resource = await import(`./locales/${lng}/translation.json`)
    i18n.addResourceBundle(lng, 'translation', resource.default)
  } catch {
    console.warn(`Failed to load language: ${lng}`)
  }
}

i18n.on('languageChanged', loadLanguage)

export default i18n
