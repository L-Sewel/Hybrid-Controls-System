#include "Valve.h" 

    // Constructor
    Valve::Valve(int upperBound, int lowerBound){
    this->upperBound = upperBound;
    this->lowerBound = lowerBound;
    }

    //*********State functions*********
    int Valve::state(){
      if(digitalRead(upperBound) == LOW){
          return -1;
        }else if(digitalRead(lowerBound) == LOW){
          return 1;
        }else{
          return 0;
          }
      }

    String Valve::strState(){
      if(digitalRead(upperBound) == LOW){
        return "OPEN";
      }else if(digitalRead(lowerBound) == LOW){
        return "CLOSE";
      }else{
        return "UNKOWN";
        }
      }

    //*********Getters*********
    int Valve::getUpperbound(){
    return this->upperBound;
    }

    int Valve::getlowerBound(){
    return this->lowerBound;     
    }
