const esModules = ['@table-library/react-table-library/theme', '@table-library/react-table-library/material-ui', '@table-library/react-table-library/table', '@mui/material', '@mui/icons-material/Info'].join('|')
module.exports = {
  preset: 'ts-jest',
  moduleNameMapper: {
    d3: '<rootDir>/node_modules/d3/dist/d3.min.js',
    '\\.(css|less)$': '<rootDir>/test-config/mocks/styleMock.js'
  },
  testEnvironment: 'jsdom',
  rootDir: '../',
  globals: {
    'ts-jest': {
      tsConfig: '<rootDir>/test-config/tsconfig.json'
    }
  },
  coveragePathIgnorePatterns: [
    '.test.tsx',
    '.test.ts',
    'models/*'
  ],
  coverageProvider: 'babel',
  collectCoverage: true,
  coverageReporters: [
    'text',
    'html',
    'cobertura'
  ],
  coverageThreshold: {
    '../**/*': {
      functions: 50,
      lines: 75,
      statements: 75
    }
  },
  testMatch: [
    '<rootDir>/**/__tests__/**/*.(spec|test).[jt]s?(x)',
    '<rootDir>/*.(spec|test).[tj]s?(x)',
    '<rootDir>/**/*.(spec|test).[tj]s?(x)'
  ],
  testPathIgnorePatterns: ['/node_modules/'],
  collectCoverageFrom: [
    '**/*.{ts,tsx}',
    '!**/node_modules/**'
  ],
  modulePaths: [
    '<rootDir>'
  ],
  transformIgnorePatterns: [`/node_modules/(?!${esModules})`],
  reporters: [
    'default',
    [
      'jest-junit',
      {
        outputDirectory: 'TestResults',
        outputName: 'test-results.xml',
        suiteName: 'ReactViews.UnitTests'
      }
    ]
  ]
}
