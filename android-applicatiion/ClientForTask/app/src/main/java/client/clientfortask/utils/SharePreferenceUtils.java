package client.clientfortask.utils;

import android.content.Context;
import android.content.SharedPreferences;
import android.text.TextUtils;

import com.google.gson.Gson;

import client.clientfortask.obj.ServerInfo;
import client.clientfortask.obj.ServerInitObj;

public class SharePreferenceUtils {
    private String name = "client";
    private String key = "server_info";

    private SharedPreferences sp;
    private static SharePreferenceUtils instance;
    private SharedPreferences.Editor editor;

    private SharePreferenceUtils(Context context) {
        sp = context.getSharedPreferences(name, Context.MODE_PRIVATE);
        editor = sp.edit();
    }

    public void saveServerInfo(ServerInfo info){
        editor.putString(key,new Gson().toJson(info));
        editor.commit();
    }

    public ServerInfo getServerInfo(){
        String s = sp.getString(key,"");
        if (TextUtils.isEmpty( s)) return null;
        return new Gson().fromJson(s, ServerInfo.class);
    }

    public static SharePreferenceUtils getInstance(Context context) {
        if (instance == null) {
            synchronized (SharePreferenceUtils.class) {
                if (instance == null) {
                    instance = new SharePreferenceUtils(context);
                }
            }
        }
        return instance;
    }
    public void clear() {
        editor.clear();
        editor.commit();
    }

    public void saveServerInitInfo(ServerInitObj.PropertyInfo property) {
        editor.putString("server_init_info",new Gson().toJson(property));
        editor.commit();
    }

    public ServerInitObj.PropertyInfo getServerInitInfo(){
        String s = sp.getString("server_init_info","");
        if (TextUtils.isEmpty( s)) return null;
        return new Gson().fromJson(s, ServerInitObj.PropertyInfo.class);
    }
}
