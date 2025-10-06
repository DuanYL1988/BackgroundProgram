package com.example.sqlite.controller;

import com.example.sqlite.model.Menu;
import com.example.sqlite.repository.MenuRepository;
import com.example.sqlite.service.MenuServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class MenuController {

    @Autowired
    MenuServiceImpl menuService;

    /**
     * 取得各自应用的菜单
     * @param condition
     * @return
     */
    @RequestMapping(value = "/menu")
    @PostMapping
    public Object getIndexMenuByApplition(String appName,String role) {
        List<Menu> menuList = menuService.getUserMenu(appName,role);
        return CtrlCommon.success(menuList);
    }

}
