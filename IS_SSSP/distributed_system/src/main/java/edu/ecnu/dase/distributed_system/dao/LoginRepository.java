package edu.ecnu.dase.distributed_system.dao;

import java.util.List;

import javax.transaction.Transactional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import edu.ecnu.dase.distributed_system.entity.course;
import edu.ecnu.dase.distributed_system.entity.student;



@Repository
@Transactional
public interface LoginRepository extends JpaRepository<student, Integer> {

	@Modifying
	@Query(value = "insert into student(name) values(?1)", nativeQuery = true)
	public void addAnswer(String name);

	@Query(value="select * from student where name=?1 and pwd=?2", nativeQuery = true)
	public student findStudent(String name,String pwd);
	
	public student save(student s);
	
	@Query(value="select id from student where name=?1", nativeQuery = true)
	public int findStudentId(String name);
	
	@Query(value = "select cid from sc where sid=?1", nativeQuery = true)
	public List<Integer> getClassList(int sid);
	
	@Query(value="select name from course where id=?1", nativeQuery = true)
	public String findCourseName(int cid);
	
	@Query(value="select id from course", nativeQuery = true)
	public List<Integer> findTotalClasses();
	
	@Query(value="select id from course where name=?1", nativeQuery = true)
	public int findCourseId(String name);
	
	@Modifying
	@Query(value = "insert into sc(cid,sid) values(?1,?2)", nativeQuery = true)
	public void chooseClasses(int cid,int sid);
}
