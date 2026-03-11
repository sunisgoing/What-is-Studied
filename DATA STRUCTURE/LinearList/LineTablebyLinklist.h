#ifndef LINETABLEBYLINKLISST_H
#define LINETABLEBYLINKLISST_H

#include "prehead.h"

template <class T>
struct Node{
	T t;
	Node * pnext;
};

template <class T>
class CLineTablebyLinklist
{
public:
	CLineTablebyLinklist(){
		Init();
	}
	~CLineTablebyLinklist()
	{
		Destroy();
	}
	
	void Insert(uint_32 index, T t)
	{
		//create a new node 
		Node<T> *  pnew = new Node<T>;
		pnew->t = t;
		pnew->pnext = NULL;
		
		Node<T> *  pt = phead;
		if(index <= 1){//insert to head 
			//add your code here
			pnew->pnext=phead;
			phead=pnew;
		}
		else if(index > tlen){ //insert to end
			//add your code here
			while(pt->pnext!=NULL)
			    pt=pt->pnext;
			pt->pnext =pnew;	
		}
		else{//insert to middle
		    uint_32 count =1;
		    while(1){
		    	if(count ==index-1){
		    	  break;
		    	}
		    	pt=pt->pnext;
		    	count ++;
			}
			pnew->pnext =pt->pnext;
			pt->pnext=pnew; 
			//add your code here
		}
		tlen ++;
	}
	void Delete(uint_32 index)
	{
		if(tlen < 1)//no node in linklist
			return;
			
		Node<T> *  pt = phead;	
		if(index <= 1){ //delete head one
			//add your code here
			index=1;
			phead=phead->pnext;
			delete pt; 
		}
		else{
			//add your code here
			uint_32 count =1;
			while(1){
				if(count==index-1){
				  break;
				}
				pt =pt->pnext;
				count++;
			}
			Node<T>*pdel=pt->pnext;
			pt->pnext=pdel->pnext;
			delete pdel;
		}
		tlen --;
	}
	void Clear(){
		Destroy();	
	}
	uint_32 Length(){
		return tlen;
	}
	bool Isempty(){
		return (tlen>0)?true:false;
	}
	T Getdata(uint_32 index){
		Node<T> *  pt = phead;
		uint_32 count = 1;
		while(1){
			//add your code here
			if(count==index){
				  break;
			}
			pt =pt->pnext;
			count++;
		}
		return pt->t;
	}

protected:
	void Init(){
		phead = NULL;
		tlen = 0;
	}
	void Destroy(){
		//add your code here
		Node<T>*pt=phead;
		while(phead){
			Delete(1);
		}
	}

private:
	Node<T> *   phead;
	uint_32     tlen;  //锟斤拷录锟斤拷锟斤拷锟斤拷锟捷讹拷锟斤拷母锟斤拷锟? 
};

#endif
