package edu.ecnu.dase.distributed_system.entity;

import java.util.HashSet;
import java.util.Set;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.JoinTable;
import javax.persistence.ManyToMany;
import javax.persistence.Table;

@Entity
@Table(name = "course")
public class course {

	@Id
	@GeneratedValue
	private int id;
	
	@Column(name = "name")
	private String name;
	
	@ManyToMany
	@JoinTable(name="sc",joinColumns={@JoinColumn(name="cid")},inverseJoinColumns={@JoinColumn(name="sid")})
	private Set<student> students = new HashSet<student>();

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Set<student> getStudents() {
		return students;
	}

	public void setStudents(Set<student> students) {
		this.students = students;
	}
	
	
	
	
}
