// Список каналов — поисковой робот будет искать расписание для каждого
// logo: emoji или URL
// search: поисковые запросы для парсинга расписания
// epgSources: прямые источники EPG (если есть)

export const CHANNELS = [
  // ── ФЕДЕРАЛЬНЫЕ ─────────────────────────────────────────────
  {
    id: 'perviy',
    name: 'Первый канал',
    logo: '①',
    color: '#1a5fb4',
    search: ['первый канал программа передач сегодня', 'channel1 tv schedule today'],
    epgSources: [
      'https://www.1tv.ru/schedule',
      'https://tv.mail.ru/channel/1/',
    ],
    m3u8Tag: 'Первый',
  },
  {
    id: 'rossia1',
    name: 'Россия 1',
    logo: 'Р',
    color: '#c0392b',
    search: ['россия 1 программа передач сегодня', 'russia 1 tv schedule'],
    epgSources: [
      'https://russia.tv/schedule',
      'https://tv.mail.ru/channel/2/',
    ],
    m3u8Tag: 'Россия',
  },
  {
    id: 'ntv',
    name: 'НТВ',
    logo: 'НТВ',
    color: '#27ae60',
    search: ['нтв программа передач сегодня ntv schedule'],
    epgSources: [
      'https://www.ntv.ru/schedule/',
      'https://tv.mail.ru/channel/4/',
    ],
    m3u8Tag: 'НТВ',
  },
  {
    id: 'ctc',
    name: 'СТС',
    logo: 'СТС',
    color: '#8e44ad',
    search: ['стс программа передач сегодня ctc tv schedule'],
    epgSources: [
      'https://ctc.ru/schedule/',
      'https://tv.mail.ru/channel/6/',
    ],
    m3u8Tag: 'СТС',
  },
  {
    id: 'tnt',
    name: 'ТНТ',
    logo: 'ТНТ',
    color: '#e67e22',
    search: ['тнт программа передач сегодня tnt schedule'],
    epgSources: [
      'https://tnt-online.ru/program/',
      'https://tv.mail.ru/channel/9/',
    ],
    m3u8Tag: 'ТНТ',
  },
  {
    id: 'ren',
    name: 'РЕН ТВ',
    logo: 'РЕН',
    color: '#d35400',
    search: ['рен тв программа передач сегодня ren tv schedule'],
    epgSources: [
      'https://ren.tv/schedule',
      'https://tv.mail.ru/channel/7/',
    ],
    m3u8Tag: 'РЕН',
  },
  {
    id: 'dom2',
    name: 'ТНТ 4',
    logo: 'ТНТ4',
    color: '#f39c12',
    search: ['тнт4 программа передач сегодня'],
    epgSources: ['https://tv.mail.ru/channel/220/'],
    m3u8Tag: 'ТНТ4',
  },
  {
    id: 'match',
    name: 'Матч ТВ',
    logo: '⚽',
    color: '#16a085',
    search: ['матч тв программа передач сегодня match tv schedule'],
    epgSources: [
      'https://matchtv.ru/schedule',
      'https://tv.mail.ru/channel/236/',
    ],
    m3u8Tag: 'Матч',
  },
  {
    id: 'kultura',
    name: 'Культура',
    logo: '🎭',
    color: '#6c3483',
    search: ['россия культура программа передач сегодня'],
    epgSources: ['https://tv.mail.ru/channel/36/'],
    m3u8Tag: 'Культура',
  },
  {
    id: 'okrug',
    name: 'ОТР',
    logo: 'ОТР',
    color: '#2980b9',
    search: ['отр программа передач сегодня otr tv'],
    epgSources: ['https://tv.mail.ru/channel/71/'],
    m3u8Tag: 'ОТР',
  },
  {
    id: 'five',
    name: 'Пятый канал',
    logo: '5',
    color: '#1abc9c',
    search: ['пятый канал программа передач сегодня 5tv schedule'],
    epgSources: [
      'https://www.5-tv.ru/schedule/',
      'https://tv.mail.ru/channel/5/',
    ],
    m3u8Tag: 'Пятый',
  },
  {
    id: 'muz',
    name: 'Муз-ТВ',
    logo: '🎵',
    color: '#e91e63',
    search: ['муз тв программа передач сегодня muz tv'],
    epgSources: ['https://tv.mail.ru/channel/16/'],
    m3u8Tag: 'Муз',
  },
  {
    id: 'tv3',
    name: 'ТВ-3',
    logo: '③',
    color: '#7f8c8d',
    search: ['тв3 программа передач сегодня tv3 schedule'],
    epgSources: ['https://tv.mail.ru/channel/11/'],
    m3u8Tag: 'ТВ3',
  },
  {
    id: 'friday',
    name: 'Пятница!',
    logo: '🎉',
    color: '#f1c40f',
    search: ['пятница тв программа передач сегодня friday tv'],
    epgSources: ['https://tv.mail.ru/channel/235/'],
    m3u8Tag: 'Пятница',
  },
  {
    id: 'zvezda',
    name: 'Звезда',
    logo: '⭐',
    color: '#c0392b',
    search: ['звезда тв программа передач сегодня zvezda tv'],
    epgSources: ['https://tv.mail.ru/channel/32/'],
    m3u8Tag: 'Звезда',
  },
];

// Источники M3U8 плейлистов (твои репо)
export const PLAYLIST_SOURCES = [
  'https://raw.githubusercontent.com/oinktechllc/livem3u/main/live.m3u',
  'https://raw.githubusercontent.com/oinktechllc/livem3u/main/playlist.m3u',
  'https://raw.githubusercontent.com/oinktechltd/rulive/main/live.m3u',
  'https://raw.githubusercontent.com/oinktechltd/rulive/main/playlist.m3u',
  'https://raw.githubusercontent.com/oinktechllc/livem3u/refs/heads/main/live.m3u',
];

// Источники CDN плеера (твои репо)
export const PLAYER_SOURCES = [
  'https://cdn.jsdelivr.net/gh/oinktechltd/cdnplayerjs@main/player.js',
  'https://cdn.jsdelivr.net/gh/twixoffltdco/cdnplayerjs@main/player.js',
  'https://cdn.jsdelivr.net/gh/oinktechllc/cdnplayerjs@main/player.js',
];
