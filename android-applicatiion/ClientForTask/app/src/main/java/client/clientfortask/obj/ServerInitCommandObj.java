package client.clientfortask.obj;

import java.util.List;

public class ServerInitCommandObj {

    /**
     * command : Initialize
     * data : {"age":23,"rest_time":60,"warm_up_time":15,"rest_heartbeat_rate":65,"fitbit_user_id":"","fitbit_user_secret":"","default_color":[255,255,255],"anaerobic_color":[153,204,51],"maximum_color":[255,68,0]}
     */

    private String command;
    private DataBean data;

    public String getCommand() {
        return command;
    }

    public void setCommand(String command) {
        this.command = command;
    }

    public DataBean getData() {
        return data;
    }

    public void setData(DataBean data) {
        this.data = data;
    }

    public static class DataBean {
        /**
         * age : 23
         * rest_time : 60
         * warm_up_time : 15
         * rest_heartbeat_rate : 65
         * fitbit_user_id :
         * fitbit_user_secret :
         * default_color : [255,255,255]
         * anaerobic_color : [153,204,51]
         * maximum_color : [255,68,0]
         */

        private int age;
        private int rest_time;
        private int warm_up_time;
        private int rest_heartbeat_rate;
        private String fitbit_user_id;
        private String fitbit_user_secret;
        private List<Integer> default_color;
        private List<Integer> anaerobic_color;
        private List<Integer> maximum_color;

        public int getAge() {
            return age;
        }

        public void setAge(int age) {
            this.age = age;
        }

        public int getRest_time() {
            return rest_time;
        }

        public void setRest_time(int rest_time) {
            this.rest_time = rest_time;
        }

        public int getWarm_up_time() {
            return warm_up_time;
        }

        public void setWarm_up_time(int warm_up_time) {
            this.warm_up_time = warm_up_time;
        }

        public int getRest_heartbeat_rate() {
            return rest_heartbeat_rate;
        }

        public void setRest_heartbeat_rate(int rest_heartbeat_rate) {
            this.rest_heartbeat_rate = rest_heartbeat_rate;
        }

        public String getFitbit_user_id() {
            return fitbit_user_id;
        }

        public void setFitbit_user_id(String fitbit_user_id) {
            this.fitbit_user_id = fitbit_user_id;
        }

        public String getFitbit_user_secret() {
            return fitbit_user_secret;
        }

        public void setFitbit_user_secret(String fitbit_user_secret) {
            this.fitbit_user_secret = fitbit_user_secret;
        }

        public List<Integer> getDefault_color() {
            return default_color;
        }

        public void setDefault_color(List<Integer> default_color) {
            this.default_color = default_color;
        }

        public List<Integer> getAnaerobic_color() {
            return anaerobic_color;
        }

        public void setAnaerobic_color(List<Integer> anaerobic_color) {
            this.anaerobic_color = anaerobic_color;
        }

        public List<Integer> getMaximum_color() {
            return maximum_color;
        }

        public void setMaximum_color(List<Integer> maximum_color) {
            this.maximum_color = maximum_color;
        }
    }
}
