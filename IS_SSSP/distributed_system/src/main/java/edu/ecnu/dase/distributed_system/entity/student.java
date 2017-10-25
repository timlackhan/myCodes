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
@Table(name = "student")
public class student {
	
	@Id
	@GeneratedValue
	private int Id;
	
	@Column(name = "name")
	private String name;
	
	@Column(name="pwd")
	private String pwd;
	
	@ManyToMany
	@JoinTable(name="sc",joinColumns={@JoinColumn(name="sid")},inverseJoinColumns={@JoinColumn(name="cid")})
	private Set<course> courses = new HashSet<course>();
	
	public int getId() {
		return Id;
	}

	public void setId(int Id) {
		this.Id = Id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getPwd() {
		return pwd;
	}

	public void setPwd(String pwd) {
		this.pwd = pwd;
	}

	public Set<course> getCourses() {
		return courses;
	}

	public void setCourses(Set<course> courses) {
		this.courses = courses;
	}

	
	
}
