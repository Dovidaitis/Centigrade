void read_uid(){
  // resets global P_UID variable to the ID which was found
  
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()){
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()){
    return;
  }

  G_UID = "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     G_UID.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
     G_UID.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
//  Serial.println(G_UID);

}
