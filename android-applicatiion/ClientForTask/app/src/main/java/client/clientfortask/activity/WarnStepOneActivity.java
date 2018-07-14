package client.clientfortask.activity;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.SwitchCompat;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import client.clientfortask.R;
import client.clientfortask.manager.ClientManager;

public class WarnStepOneActivity extends BaseActivity implements View.OnClickListener, CompoundButton.OnCheckedChangeListener {

    private TextView settings;
    private TextView start;
    private SwitchCompat btn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_warn_step_one);

        settings = findViewById(R.id.settings);
        start = findViewById(R.id.start);
        btn = findViewById(R.id.switch_btn);

        settings.setOnClickListener(this);
        start.setOnClickListener(this);
        btn.setOnCheckedChangeListener(this);
    }

    @Override
    public void onClick(View v) {
        if (v == start) {
            Intent intent = new Intent(this, ServerInitActivity.class);
            startActivity(intent);
            finish();
        }else if (v== settings){
            Intent intent = new Intent(this,SettingsActivity.class);
            startActivity(intent);
        }
    }

    @Override
    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
            JSONObject object = new JSONObject();
            try {
                object.put("command", "Set demo module");
                ClientManager.getInstance().sendData(object.toString());
            } catch (JSONException e) {
                e.printStackTrace();
            }

    }
}
