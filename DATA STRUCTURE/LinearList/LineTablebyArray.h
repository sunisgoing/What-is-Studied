#ifndef LINETABLEBYARRAY_H
#define LINETABLEBYARRAY_H

#include "prehead.h"  

#define SIZE_ADD  100

template <class T>
class CLineTablebyArray
{
public:
	CLineTablebyArray(){
		Init();
	}
	~CLineTablebyArray()
	{
		Destroy();
	}
	//index: array index from 1 to ...
	void Insert(uint_32 index, T t)
	{
		if(index > tlen+1 ){  //check index validity 
			index = tlen+1;
		}
		//if need allocate more storage space 
		if(tlen == tsize){
			T*pnew=new T [tsize + SIZE_ADD];
			memcpy(pnew,pt,tlen*sizeof(T));
			delete [] pt;
			pt=pnew;
			tsize+=SIZE_ADD;
			//add your code here
		}
		//move data
		index = (index <= 0)?1:index;
		Move(index,true);

		//insert
		pt[index-1]=t;
		tlen++;
		
		//add your code here
	}
	void Delete(uint_32 index)
	{
		//check index validity
		if(index > tlen)
			return;
		//delete
		index = (index <= 0)?1:index;
		Move(index, false);
		tlen --;
		//free up space
		Reclaim(2);	
	}
	void Clear(){
		tlen = 0;
		Reclaim(1);	
	}
	uint_32 Length(){
		return tlen;
	}
	bool Isempty(){
		return (tlen>0)?true:false;
	}
	T Getdata(uint_32 index){
		if(tlen == 0){
			T a;
			memset(&a,0,sizeof(T));
			return a;
		}
		else if(index > tlen){
			return pt[0]; 
		}
		else{
			index=(index<=0)?1:index;
			return pt[index-1];
			//add your code here;
		}		
	}

protected:
	void Init(){
		pt = new T [SIZE_ADD];
		tlen = 0;
		tsize = SIZE_ADD;
	}
	void Destroy(){
		tlen=0;
		tsize=0;
		if(pt)
		  delete [] pt;
		//add your code here;
	}
	void Move(uint_32 index, bool flag){
		if(flag == true){ //backward
		    memcpy(pt+index,pt+index-1,(tlen-index+1)*sizeof(T));
			//add your code here;
		}
		else{ //forward
		    memcpy(pt+index-1,pt+index,(tlen-index)*sizeof(T));
			//add your code here;
		} 
	}
	void Reclaim(uint_32 factor){
		if(tsize - tlen >= SIZE_ADD *factor){
			//add  your code here;	
			tsize =(tlen/SIZE_ADD+1)*SIZE_ADD;
			T*pnew=new T [tsize];
			memcpy(pnew,pt,tlen*sizeof(T));
			delete [] pt;
			pt=pnew; 
		}
	}
private:
	T *     pt;
	uint_32 tlen;  //data number 
	uint_32 tsize; //allocated space 
};

#endif
