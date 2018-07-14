package client.clientfortask.obj;

import android.app.Activity;

import java.util.ArrayList;
import java.util.List;

public class Mode {
    private static Mode instance;
    private int age;
    private int heart;
    private Mode(){};
    public static synchronized Mode getInstance(){
        if (instance == null) instance = new Mode();
        return instance;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public int getHeart() {
        return heart;
    }

    public void setHeart(int heart) {
        this.heart = heart;
    }
}
