package com.example.sqlite.service;

import com.example.sqlite.model.Menu;
import com.example.sqlite.repository.MenuRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MenuServiceImpl {

    @Autowired
    private MenuRepository menuDao;

    public List<Menu> getAllMenu(){
        Menu condition = new Menu();
        return menuDao.selectByDto(condition);
    }

    public List<Menu> getUserMenu(String appName, String role) {
        Menu condition = new Menu();
        condition.setApplication(appName);
        condition.setCompGroup(role);
        return menuDao.selectByDto(condition);
    }
}
