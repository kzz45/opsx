/* eslint-disable */

import defaultSettings from '@/settings'

const title = defaultSettings.title || 'DOPS'

export default function getPageTitle(pageTitle) {
    if (pageTitle) {
        return `${pageTitle} - ${title}`
    }
    return `${title}`
}