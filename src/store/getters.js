/* eslint-disable */

const getters = {
  sidebar: (state) => state.app.sidebar,
  device: (state) => state.app.device,
  token: (state) => state.user.token,
  avatar: (state) => state.user.avatar,
  name: (state) => state.user.name,
  user_id: (state) => state.user.user_id,
  is_superuser: (state) => state.user.is_superuser,
  roles: (state) => state.user.roles,
  permission_routes: (state) => state.permission.routes,
  product_list: (state) => state.product.product_list,
  current_select_product_id: (state) => state.product.current_select_product_id,
  current_select_product_name: (state) =>
    state.product.current_select_product_name,
};
export default getters;
