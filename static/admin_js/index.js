const app = new Vue({
    el: '#app',
    data() {
      return {
        coin: 'just a coin',
        coins: null,
      };
    },
    created() {
      // Assuming ws_scheme and web_socket_url are defined
      const socket = new WebSocket(`${ws_scheme}://${web_socket_url}/ws/testWebsocket/`);
      const _this = this;
  
      socket.onmessage = function (event) {
        _this.coins = JSON.parse(event.data);
        if ("connection" in _this.coins) {
          console.log('Websocket connected...');
        } else {
          handleLiveData(_this.coins);
        }
      };
  
      // Add other event handlers (onclose, onerror) as needed
  
      // Close the socket when the component is destroyed to prevent memory leaks
      this.$options.beforeDestroy = function () {
        socket.close();
      };
    },
  });
  
  
  