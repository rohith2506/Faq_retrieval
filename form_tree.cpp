#include <iostream>
#include <stdio.h>
#include <zmq.hpp>
#include <stack>
#include <cmath>
#include <cstring>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <queue>
using namespace std;
const int lambda = 0.5;
const int mu = 0.5;

struct node{
	string str;
	int size;
	int depth;
	int label;
	bool terminal;
	vector<int> indexes;
	vector<node *> child;
}*root;    

class form_tree{
public:
	node *main_func(string str);
	node *main_function(string parse_quest);
	void depth(node *t ,int dpt);
	int size(node *t);
	void size1(node *t);
	void level_order(node *t);
	void assign_child(node *t);
	int total_fragments(node *t);
	node* get(node *t,int pos);
	double delta(string str);
	double calculate(node *t1,node *t2);
	void parse_tree(string parse_quest,vector<string> test_quest);
};

node * form_tree :: main_func(string quest){
	stack<node *> stk;
	node *temp = new node;
	stringstream ss;
	ss << quest[0];
	ss >> temp -> str;
	stk.push(temp);

//	cout << quest << endl;
	for(int i=1;i<quest.length();i++){
		if(quest[i] == ')' || quest[i] == '('){
			if(quest[i] == ')'){
//				cout << "iam here again after closed bracket" << endl;
				vector<node *> children;
				while(stk.top()->str!="("){
					node *temp2 = stk.top();
					children.push_back(temp2);
					stk.pop();
				}
				stk.pop();
				node *temp3 = new node;
				int sz = children.size();
				temp3 -> str = children[sz-1] -> str;
				for(int j=0;j<children.size()-1;j++)
					temp3 -> child.push_back(children[j]);
//				cout << "After closed bracket " << temp3 -> str << endl;
				stk.push(temp3);
			}
			else{
				node *temp4 = new node;
				stringstream ss2;
				ss2 << quest[i];
				ss2 >> temp4->str;
				stk.push(temp4);
			}
		}
		else{
			string str2 = "";
			int j=i;
			while(quest[j]!=' '){	
				str2 = str2 + quest[j];
				if(quest[j+1] == ')')
					break;
				j++;
			}
			node *temp5 = new node;
			temp5 -> str = str2;
			stk.push(temp5);
			i = j;
		}
	}
	node *main_root = stk.top();
	depth(main_root,1);
	main_root -> size = size(main_root);
	size1(main_root);
	level_order(main_root);
//	cout << main_root -> child[0] -> child[4] -> child[0] -> child[0] ->label << " " << main_root  -> child[0] -> child[4] -> child[0] -> child[0] -> terminal << endl;
	assign_child(main_root);
	return main_root;
}


node *form_tree::main_function(string parse_quest){
	node *t = new node();
	t=main_func(parse_quest);
	return t;
}

// to assign size and depth for each node

void form_tree::depth(node *t,int dpt){
	if(t -> child.size() == 0)
		return ;
	else{
		t -> depth = dpt;
		dpt++;
		for(int i=0;i<t->child.size();i++)
			depth(t->child[i],dpt);
	}
}

int form_tree::size(node *t){
	if(t -> child.size() == 0)
		return 0;
	else{
		int x = t->child.size();
		for(int i=0;i<t->child.size();i++) 
			x = x + size(t->child[i]);
		return x;
	}
}

void form_tree::size1(node *t){
	for(int i=0;i<t->child.size();i++){
		int sz = size(t->child[i]);
		t->child[i]->size=sz;
		size1(t->child[i]);
	}
}


void form_tree::level_order(node *t){
	queue<node *> q;
	int idx = 1;
	q.push(t);
	while(!q.empty()){
		node *t1 = q.front();
		q.pop();
		t1->label = idx; 
		if(t1->child.size() == 0)
			t1->terminal = true;
		for(int i=0;i<t1->child.size();i++)
			q.push(t1->child[i]);			
		idx++;
	}	
}


void form_tree::assign_child(node *t){
	for(int i=0;i<t->child.size();i++){
		t->indexes.push_back(t->child[i]->label);	
		assign_child(t->child[i]);
	}
}


//Main part comes here
//calculating M(r1,r2)


int form_tree::total_fragments(node *t){
	queue<node *> q;
	int idx = 0;
	q.push(t);
	while(!q.empty()){
		node *t1 = q.front();
		q.pop();
		for(int i=0;i<t1->child.size();i++)
			q.push(t1->child[i]);			
		idx++;
	}
	return idx;	
}

node *form_tree::get(node *t,int pos){
	queue<node *> q;
	int idx = 0;
	q.push(t);
	while(!q.empty()){
		if(idx == pos)
			return q.front();
		node *t1 = q.front();
		q.pop();
		for(int i=0;i<t1->child.size();i++)
			q.push(t1->child[i]);			
		idx++;
	}	
}

double form_tree::delta(string str){
	if(str == "VB" || str == "NN")
		return 1.2;
	else if(str == "VP" || str == "NP")
		return 1.1;
	else
		return 1;
}

double form_tree::calculate(node *t1,node *t2){
	int T1 = total_fragments(t1);
	int T2 = total_fragments(t2);
//	cout << T1  << " " << T2 << endl;

	int eta = 0;
	vector<vector<double> > M(T1,vector<double>(T2,0));
	for(int i=T1-1;i>=0;i--){
		for(int j=T2-1;j>=0;j--){
			//if r1 and r2 are terminals
			node *t3 = get(t1,i);
			node *t4 = get(t2,j);

//			cout << t3->terminal << " " << t4 -> terminal << endl;
			if(t3 -> terminal == true && t4 -> terminal == true){
				if(t3 -> str != t4 -> str)
					M[i][j] = 0;
				else{
					eta++;
					M[i][j] = delta(t3->str) * delta(t4->str) * pow(lambda,t3->size + t4->size) * pow(mu,t3->depth + t4->depth);
				}
			}
			else{
					eta++;
					int r1 = t3 -> child.size();
					int r2 = t4 -> child.size();
					int val = std::min(r1,r2);
					node * temp;
					if(val == r1)
						temp = t3;
					else
						temp = t4;
					int result = 0;
//					cout << val << endl;
					for(int k=0;k<val;k++){
//						cout << t3->child[k]->label << " " << t4->child[k]->label << endl;
						result = result * M[t3->child[k]->label-1][t4->child[k]->label-1];
					}
					M[i][j] = result * pow(delta(t3->str),eta) * pow(delta(t4->str),eta) * pow(lambda,2*eta) * pow(mu,eta * (2 -(1 + temp -> child.size())*(t3->depth + t4->depth)));
			}
		}
	}
	int main_result = 0;
	for(int i=0;i<M.size();i++){
		for(int j=0;j<M[i].size();j++){
			main_result = main_result + M[i][j];
		}
	}
	cout << main_result << endl;
	return main_result;
}

void form_tree :: parse_tree(string parse_quest,vector<string> test_quest){
	ifstream fin;
	fin.open("test3.txt");
	string res2,line;
	while(getline(fin,line))
		res2 = line;
	node *main_root = main_function(parse_quest);
	vector<node *> parse;
	for(int i=0;i<test_quest.size();i++)
		parse.push_back(main_function(test_quest[i]));

	string res = "";
	double maxres = 0;
	for(int i=0;i<parse.size();i++){
		double temp_res = calculate(main_root,parse[i]);
		if(temp_res > maxres){
			maxres = temp_res;
			res = test_quest[i];
		}
	}
	res = res2;
	cout << "Result is: " << res << endl;
}

int main(int argc,char *argv[]){
	zmq::context_t context (1);
	zmq::socket_t socket (context, ZMQ_REP);
	socket.bind ("tcp://127.0.0.1:5000");

	while (true) {
		cout<<"iam here"<<endl;
        zmq::message_t request,request2;
        socket.recv (&request);
        cout <<"iam here tweoooo"<<endl;
		char *num = (char *) request.data();
        string parse_quest = "";

        int i;
       	for(i=0;i<strlen(num);i++){
        	if(num[i] == '\n')
        		break;
        	parse_quest = parse_quest + num[i];
        }
        cout << parse_quest << endl;

        vector<int> train_quest;
        int val = 0;

        for(int j=i;j<strlen(num);j++){
        	if(num[j] == '$'){
        		train_quest.push_back(val);
        		val = 0;
        	}
        	else
        		val = val * 10 + (int)(num[j] - '0');
        }

        ifstream fin;
        vector<string> parse;
        fin.open("kernel_trees.txt");
        string line;
       	int line_cnt = 1;

        while(getline(fin,line)){
        	for(int i=0;i<train_quest.size();i++){
        		if(train_quest[i] == line_cnt){
        			parse.push_back(line);
        			break;
        		}
        	}
        	line_cnt = line_cnt + 1;
        }
        
        form_tree obj;
        obj.parse_tree(parse_quest,parse);
        sleep (1000);
    }
    return 0;
}