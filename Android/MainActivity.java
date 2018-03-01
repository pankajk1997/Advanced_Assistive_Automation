package com.quickclip.panky.quickclip;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

import java.io.ByteArrayOutputStream;
import java.util.Properties;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    EditText e1;
    Button b1,b2,b3;
    TextView t1;
    Activity activity = this;
    static int flag=2,time=3000;
    static ClipData clip=null;
    String output;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        e1 = (EditText) findViewById(R.id.editText);
        t1 = (TextView) findViewById(R.id.textView);
        b1 = (Button) findViewById(R.id.button1);
        b2 = (Button) findViewById(R.id.button2);
        b3 = (Button) findViewById(R.id.button3);

        getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_VISIBLE);

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                CopyMethod();
            }
        });

        b2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                VolDown();
            }
        });

        b3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                CopyPace();
            }
        });

        Runnable myRunnable = new Runnable() {
            @Override
            public void run() {
                while (true) {
                    if (flag % 2 == 0) {
                        try {
                            Thread.sleep(time);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    } else if (flag % 2 != 0) {
                        try {
                            Thread.sleep(800);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                    activity.runOnUiThread(new Runnable() {
                        public void run() {
                            CopyMethod();
                            flag += 1;
                        }
                    });
                }
            }
        };

        Thread myThread = new Thread(myRunnable);
        myThread.start();
    }

    public void VolDown(View view) {VolDown();}
    public void CopyPace(View view) {CopyPace();}
    public void ManCopy(View view) {CopyMethod();}

    public void VolDown() {
        e1.setText("decrease volume");
    }

    public void CopyPace() {
        if(time==5000) time=2000;
        else if(time<5000) time+=1000;
        t1.setText("Automatically Sending in: "+(time/1000)+" sec");
    }

    public void CopyMethod() {

        final String username="pi";
        final String password="10<,mmXLSQ";
        final String hostname="192.168.43.41";
        final int port=22;
        final String a="echo '",c="' > /home/pi/Documents/HAP/input.txt";

        ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
        final ClipData clip = ClipData.newPlainText("Copied Text", (CharSequence) e1.getText().toString());
        clipboard.setPrimaryClip(clip);

        new AsyncTask<Integer, Void, Void>(){
            @Override
            protected Void doInBackground(Integer... params) {
                try {
                    JSch jsch = new JSch();
                    Session session = jsch.getSession(username, hostname, port);
                    session.setPassword(password);

                    // Avoid asking for key confirmation
                    Properties prop = new Properties();
                    prop.put("StrictHostKeyChecking", "no");
                    session.setConfig(prop);

                    session.connect();

                    // SSH Channel
                    ChannelExec channelSsh = (ChannelExec)
                            session.openChannel("exec");
                    ByteArrayOutputStream baos = new ByteArrayOutputStream();
                    channelSsh.setOutputStream(baos);

                    // Execute command
                    String cmd=a+clip+c;
                    channelSsh.setCommand(cmd);
                    channelSsh.connect();
                    channelSsh.disconnect();

                } catch (Exception e) {
                    e.printStackTrace();
                }
                return null;
            }
        }.execute(1);

        e1.setText("");
    }

    @Override
    public void onClick(View view) {CopyMethod();VolDown();CopyPace();}
}