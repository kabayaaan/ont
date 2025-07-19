export default {
  server: {
    port: 5173,
    proxy: {
      '/inject-nat': 'http://backend:8000'
    }
  }
}
