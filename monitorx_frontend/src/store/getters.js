/* eslint-disable */

const getters = {
    sidebar: state => state.app.sidebar,
    device: state => state.app.device,
    token: state => state.user.token,
    id_token: state => state.user.id_token,
    avatar: state => state.user.avatar,
    name: state => state.user.name,
    user_id: state => state.user.user_id,
    is_superuser: state => state.user.is_superuser,
    roles: state => state.user.roles,
    groups: state => state.user.groups,
    group_roles: state => state.user.group_roles,
    is_ops: state => state.user.is_ops,
    users: state => state.user_list.users,
    global_product_list: state => state.global_product.global_product_list,
    global_product_map: state => state.global_product.global_product_map,
    current_select_product_id: state => state.global_product.current_select_product_id,
    current_select_product_name: state => state.global_product.current_select_product_name,
}
export default getters

