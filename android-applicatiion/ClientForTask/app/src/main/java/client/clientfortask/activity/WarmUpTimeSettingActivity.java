package client.clientfortask.activity;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.text.TextUtils;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.greenrobot.eventbus.EventBus;

import client.clientfortask.R;
import client.clientfortask.obj.WarmUpTimeObj;

public class WarmUpTimeSettingActivity extends BaseActivity implements View.OnClickListener {
    private EditText time;
    private View ok;
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_warm_up);
        time = findViewById(R.id.age);
        ok = findViewById(R.id.ok);
        ok.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        if (TextUtils.isEmpty(time.getText().toString())){
            Toast.makeText(this, "Please enter the time!", Toast.LENGTH_SHORT).show();
            return;
        }
        WarmUpTimeObj obj = new WarmUpTimeObj();
        obj.time = Integer.parseInt(time.getText().toString());
        obj.type = 0;
        EventBus.getDefault().post(obj);
        finish();
    }
}
