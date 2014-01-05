#include "mongo/client/dbclient.h"
#include <stdio.h>
#include <cstdlib>
#include <stdlib.h>
#include <iostream>

#define ID_LEN 	24
#define N_CHILD	36

using std::vector;
using std::string;
using std::auto_ptr;

int
get_idx(char c)
{
    if (c >= '0' && c <= '9')
        return c - '0';
    return c - 'A' + 10;
}

class S_List {
public:
    S_List 	*next;
    string	*id;

    S_List(string *id, S_List *next);
    ~S_List(void);
};

S_List::~S_List(void)
{
    //std::cout << "OH! I'm dead! ======== S_List" << std::endl;
    if (this->next != NULL)
	delete this->next;
}

S_List::S_List(string *id, S_List *next)
{
    this->id = id;
    this->next = next;
}

class Py_Tree {
public:
    Py_Tree 		*next[N_CHILD];
    S_List 		*ids;
    
    Py_Tree(void);
    ~Py_Tree(void);

    Py_Tree *make_node(void);	
    void fresh(string *py, string *id);
    void add_Id(string *id);
    Py_Tree *search(const char *s);
    Py_Tree *search(string s);
};

Py_Tree *
Py_Tree::search(const char *s)
{
    Py_Tree *itree = this;
    for (int i = 0, len = strlen(s); i < len; i++) {
	itree = itree->next[get_idx(s[i])];
	if (itree == NULL)
	    return NULL;
    }

    return itree;
}

Py_Tree *
Py_Tree::search(string s)
{
    return this->search(s.c_str());
}

void
Py_Tree::add_Id(string *id)
{
    this->ids = new S_List(id, this->ids);
}

Py_Tree::~Py_Tree(void)
{
    //std::cout << "OH! I'm dead!" << std::endl;
    delete this->ids;

    for (int i = 0; i < N_CHILD; i++)
	if (this->next[i] != NULL)
	    delete this->next[i];
}

Py_Tree::Py_Tree(void)
{
    for (int i = 0; i < N_CHILD; i++)
    	next[i] = NULL;
    ids = NULL;
}


Py_Tree *
Py_Tree::make_node(void)
{
    return new Py_Tree();
}

void
Py_Tree::fresh(string *py, string *id)
{
    if (id->length() != 24) {
	std::cout << "[ERROR in Py_Tree::fresh()]: Bad id -> " << id << std::endl;
	return;
    }

    Py_Tree *itree, *node;
    for (int len = py->length(), i = len - 1; i >= 0; i--) {
	itree = this;
	for (int j = i; j < len; j++) {
	    int idx = get_idx(py->at(j));
	    node = itree;
	    if ((itree = itree->next[idx]) == NULL)
		itree = node->next[idx] = new Py_Tree();
	}
	itree->add_Id(id);
    }
}

void
pr_ids(S_List *ids)
{
    for (S_List *id = ids; id != NULL; id = id->next)
	std::cout <<  *(id->id) << '\t';
    std::cout << std::endl;
}

void
pr_tree(Py_Tree *tree)
{
    if (tree == NULL)
        return;

    //printf("good\n");
    for (int i = 0; i < N_CHILD; i++) {
        if (tree->next[i] != NULL) {
            printf("%d\n", i);
            pr_tree(tree->next[i]);
        }
    }

    pr_ids(tree->ids);
}

int
main(void)
{
    Py_Tree *pt = new Py_Tree();

#define host "sz.togic.com"
#define db string("newhao123")
    mongo::DBClientConnection mc;
    mc.connect(host);
    int cnt = mc.count(db + ".pinyin_index");
    std::cout << cnt << std::endl;

    auto_ptr<mongo::DBClientCursor> cursor = mc.query(db+".pinyin_index");
    char *is = new char[2];
    while (cursor->more()) {
	mongo::BSONObj item = cursor->next();
	//std::cout << item.getField("_id").__oid().toString() << std::endl;
	string *_id = new string(item.getField("_id").__oid().toString());
	//std::cout << item.getStringField("title") << std::endl;
	mongo::BSONObj py = item.getObjectField("pinyin");
	for (int i = 0; ; i++) {
	    sprintf(is, "%d", i);
	    string *s = new string(py.getStringField(is));
	    if (s->empty()) {
		delete s;
		break;
	    }
	    pt->fresh(s, _id);
	    delete s;
	}
	//std::cout << (strlen(item.getObjectField("pinyin").getStringField("3"))) << std::endl;
	//std::cout << item.toString() << std::endl;
    }

    delete is;

    pr_tree(pt->search("A"));
    //pt->fresh(new string("goodnews"), new string("egfdegfdegfdegfdegfdegfd"));
    //pr_tree(pt);
    //std::cout << *pt->next[24]->next[24]->next[13]->next[23]->next[14]->next[32]->next[28]->ids->id << std::endl;
    sleep(10);
    delete pt;
    return 0;
}
