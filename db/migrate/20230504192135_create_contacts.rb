class CreateContacts < ActiveRecord::Migration[6.1]
  def change
    create_table :contacts do |t|
      t.datetime :time_call_began
      t.datetime :time_call_ended
      t.integer :initial_counselor_id
      t.integer :total_counslors
      t.integer :total_transfers
      t.string :issues_discussed
      t.integer :call_rating
      t.integer :initial_risk_level
      t.string :client_pronouns
      t.string :client_name
      t.string :client_location
    end
  end
end
