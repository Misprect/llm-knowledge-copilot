export default {
  server: {
    port: 5173,
    proxy: {
      "/query": "http://127.0.0.1:8000",
      "/dashboard": "http://127.0.0.1:8000",
    },
  },
};
