
float get_avg_temp(){
    double temp_sum = 0.0;
    int count = 0;
    for (int i=0; i<10; i++){
      delay(1);
      double temp = mlx.readObjectTempC();
      if (temp > OUTLIER_TEMP_LOW && temp < OUTLIER_TEMP_HIGH){
        count += 1;
        temp_sum += temp;
        }
    }
  
    float temp_avg = temp_sum/count;
    if (count > 5){
      return temp_avg;
    }
    else{
      return -1;
    }
}

