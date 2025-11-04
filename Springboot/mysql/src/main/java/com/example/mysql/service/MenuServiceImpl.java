package com.example.mysql.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;

import com.example.mysql.dto.AccountDto;
import com.example.mysql.dto.MenuDto;
import com.example.mysql.model.Menu;
import com.example.mysql.repository.MenuRepository;

@Service
public class MenuServiceImpl {

    private final MenuRepository menuDao;

    public MenuServiceImpl(MenuRepository menuDao) {
        this.menuDao = menuDao;
    }

    public Map<String, List<Menu>> getAllMenu(AccountDto user) {
        // 分组菜单
        Map<String, List<Menu>> menuGroup = new HashMap<>();
        MenuDto condition = new MenuDto();
        // 条件:显示 = 1
        condition.setDisableFlag("1");
        // 设置用户可以查看的菜单权限
        if (!"ADMIN".equals(user.getApplication().toUpperCase())) {
            condition.setApplication(user.getApplication());
            // 部门分组
            if (!"ADMIN".equals(user.getRoleId().toUpperCase())) {
                condition.setCompGroup(user.getRoleId());
            }
        }
        // 全部菜单取得
        List<Menu> menuList = menuDao.selectByDto(condition);
        for (Menu menu : menuList) {
            // 根据父菜单名分组
            String groupName = menu.getParentId();
            List<Menu> childMenu = menuGroup.get(groupName);
            if (null == childMenu) {
                childMenu = new ArrayList<>();
            }
            childMenu.add(menu);
            menuGroup.put(groupName, childMenu);
        }
        return menuGroup;
    }
}
