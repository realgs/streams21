module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:prettier/recommended',
    'plugin:vue/essential',
    '@vue/prettier'
  ],
  rules: {
    'import/no-unresolved': 0,
    'import/no-unassigned-import': 0,
    'no-console': process.env.NODE_ENV === 'production' ? 'off' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off'
  },
  parserOptions: {
    parser: 'babel-eslint'
  }
}